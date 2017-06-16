"""
Copyright 2013 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import config
import json
import jwt
import logging
import os
import string
import time
import urllib
import webapp2
import wob_payload
import httplib2
import loyalty
import offer
import giftcard
import random

from apiclient.discovery import build_from_document
from apiclient.http import HttpMock
from google.appengine.ext.webapp import template
from oauth2client import crypt
from google.auth import crypt as crypt_google
from oauth2client.service_account import ServiceAccountCredentials

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with the Credentials. Note that the first parameter, service_account_name,
# is the Email address created for the Service account. It must be the email
# address associated with the key that was created.
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.SERVICE_ACCOUNT_PRIVATE_KEY,
  'https://www.googleapis.com/auth/wallet_object.issuer')
http = httplib2.Http()
http = credentials.authorize(http)

logging.info('Credentials: %s' % credentials.to_json())
f = file(config.DISCOVERY_JSON, 'rb')
disc_content = f.read()
f.close()

service = build_from_document(disc_content, http=http)


def displayIndex(request):
  """Serves the index page.

  Args:
    request: A HTTP request object.

  Returns:
    The index page.
  """
  path = os.path.join(os.path.dirname(__file__), 'index.html')
  template_values = {}
  return webapp2.Response(template.render(path, template_values))


def handleJwt(request):
  """Serves JWT response of appropriate type.

  Args:
    request: A HTTP request object.

  Returns:
    An encoded JWT object as response.
  """
  wob_payload_object = wob_payload.WOB_Payload()
  jwt_type = request.GET.get('type', '')
  obj_id = str(random.randint(1, 100))

  if jwt_type == 'loyalty':
    loyalty_obj = loyalty.generate_loyalty_object(
        config.ISSUER_ID, config.LOYALTY_CLASS_ID, config.LOYALTY_OBJECT_ID + obj_id)
    wob_payload_object.addWalletObjects(loyalty_obj, 'LoyaltyObject')

  elif jwt_type == 'offer':
    offer_obj = offer.generate_offer_object(
        config.ISSUER_ID, config.OFFER_CLASS_ID, config.OFFER_OBJECT_ID + obj_id)
    wob_payload_object.addWalletObjects(offer_obj, 'OfferObject')

  elif jwt_type == 'giftcard':
    giftcard_obj = giftcard.generate_giftcard_object(
        config.ISSUER_ID, config.GIFTCARD_CLASS_ID, config.GIFTCARD_OBJECT_ID + obj_id)
    wob_payload_object.addWalletObjects(giftcard_obj, 'GiftCardObject')

  payload = wob_payload_object.getSaveToWalletRequest()
  signer = crypt_google.RSASigner.from_service_account_file(config.SERVICE_ACCOUNT_PRIVATE_KEY)
  signed_jwt = crypt.make_signed_jwt(signer, payload)

  response = webapp2.Response(signed_jwt)
  response.content_type = 'Application/JWT'
  return response


def handleInsert(request):
  """Make API call to insert a new loyalty or offer class.

  Args:
    request: A HTTP request object.

  Returns:
    The result indicating success/failure of the API call to insert the class.
  """
  insert_type = request.GET.get('type', '')

  if insert_type == 'loyalty':
    object_id = config.LOYALTY_CLASS_ID
    api_object = loyalty.generate_loyalty_class(
      config.ISSUER_ID, object_id)
    collection = service.loyaltyclass()
  elif insert_type == 'offer':
    object_id = config.OFFER_CLASS_ID
    api_object = offer.generate_offer_class(
      config.ISSUER_ID, object_id)
    collection = service.offerclass()
  elif insert_type == 'giftcard':
    object_id = config.GIFTCARD_CLASS_ID
    api_object = giftcard.generate_giftcard_class(
      config.ISSUER_ID, object_id)
    collection = service.giftcardclass()
  api_request = collection.insert(body=api_object)
  api_response = api_request.execute()
  response = webapp2.Response('Successfully inserted object')
  if 'error' in api_response.keys():
    response = webapp2.Response('Error inserting object %s' % object_id)
  return response


def handleWebservice(request):
  """Creates wallet object according to webservice requests.

  Args:
    request: A HTTP request object.

  Returns:
    Returns object on success, or, error on failure.
  """
  jsonobj = json.loads(request.body)
  first_name = jsonobj['params']['walletUser']['firstName']
  #using first_name to test different error codes
  success = (first_name.startswith('SUCCESS'))

  if success:
    #possible success status codes:
    #SUCCESS, SUCCESS_ACCOUNT_ALREADY_CREATED, SUCCESS_ACCOUNT_ALREADY_LINKED
    jwt = {
      'iss': config.SERVICE_ACCOUNT_EMAIL_ADDRESS,
      'aud': config.AUDIENCE,
      'typ': config.LOYALTY_WEB,
      'iat':  int(time.time()),
      'payload': {
        'loyaltyObjects': [],
        'webserviceResponse': {
          'status': 'SUCCESS'
        },
      }
    }
    linking_id = request.params.get('linkingId')
    loyalty_object_id = linking_id if linking_id else config.LOYALTY_OBJECT_ID
    loyalty_object = loyalty.generate_loyalty_object(
        config.ISSUER_ID, config.LOYALTY_CLASS_ID, loyalty_object_id)
    jwt['payload']['loyaltyObjects'].append(loyalty_object)
  else:
    #possible status error codes:
    #ERROR_INVALID_DATA_FORMAT, ERROR_DATA_ON_MERCHANT_RECORD_DIFFERENT
    #ERROR_INVALID_LINKING_ID, ERROR_PREEXISTING_ACCOUNT_REQUIRES_LINKING, ERROR_ACCOUNT_ALREADY_LINKED
    error_action = 'link' if request.params.get('linkingId') else 'signup'
    jwt = {
      'iss': config.SERVICE_ACCOUNT_EMAIL_ADDRESS,
      'aud': config.AUDIENCE,
      'typ': config.LOYALTY_WEB,
      'iat':  int(time.time()),
      'payload': {
        'webserviceResponse': {
          'status': 'ERROR_INVALID_DATA_FORMAT',
          'invalidWalletUserFields': ['zipcode','phone']
        },
      }
    }
  signer = crypt.Signer.from_string(key)
  signed_jwt = crypt.make_signed_jwt(signer, jwt)
  response = webapp2.Response(signed_jwt)
  response.content_type = 'Application/JWT'
  return response


def handleList(request):
  """List wallet object according to parameters.

  Args:
    request: A HTTP request object.

  Returns:
    List of wallet objects
  """
  wob_type = request.GET.get('type', '')
  class_id = request.GET.get('class_id', '')
  print (wob_type)
  if wob_type == 'loyalty_class':
    results = service.loyaltyclass().list(issuerId=config.ISSUER_ID,
      maxResults='25').execute()
    results = service.loyaltyclass().list(issuerId=config.ISSUER_ID).execute()
  elif wob_type == 'offer_class':
    results = service.offerclass().list(issuerId=config.ISSUER_ID,
      maxResults='25').execute()
  elif wob_type == 'giftcard_class':
    results = service.giftcardclass().list(issuerId=config.ISSUER_ID,
      maxResults='25').execute()
  elif wob_type == 'loyalty_object':
    results = service.loyaltyobject().list(classId=class_id,
      maxResults='100').execute()
  elif wob_type == 'offer_object':
    results = service.offerobject().list(classId=class_id,
      maxResults='25').execute()
  elif wob_type == 'giftcard_object':
    results = service.giftcardobject().list(classId=class_id,
      maxResults='25').execute()
  print results['pagination']['resultsPerPage']
  if 'nextPageToken' in results['pagination']:
    print results['pagination']['nextPageToken']
  for wallet_object in results['resources']:
    print wallet_object['id']


application = webapp2.WSGIApplication([
    ('/', displayIndex),
    ('/jwt', handleJwt),
    ('/insert', handleInsert),
    ('/list', handleList),
    ('/webservice', handleWebservice)
    ])
