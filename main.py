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
import loyalty
import offer
import os
import string
import time
import urllib
import webapp2
import wob_payload

from apiclient.discovery import build
from apiclient.http import HttpMock
from google.appengine.ext.webapp import template
from oauth2client import crypt


with open(os.path.join(os.path.dirname(__file__), config.KEY_FILE)) as fp:
  app_key = string.join(fp.readlines())

http = HttpMock(
    os.path.join(os.path.dirname(__file__), config.DISCOVERY_JSON),
    {'status': '200'})
service = build('walletobjects', 'v1', http=http, developerKey=app_key)


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

  if jwt_type == 'loyalty':
    loyalty_obj = loyalty.generate_loyalty_object(
        config.ISSUER_ID, config.LOYALTY_CLASS_ID, config.LOYALTY_OBJECT_ID)
    wob_payload_object.addWalletObjects(loyalty_obj, 'LoyaltyObject')

  elif jwt_type == 'offer':
    offer_obj = offer.generate_offer_object(
        config.ISSUER_ID, config.OFFER_CLASS_ID, config.OFFER_OBJECT_ID)
    wob_payload_object.addWalletObjects(offer_obj, 'OfferObject')

  payload = wob_payload_object.getSaveToWalletRequest()
  signer = crypt.Signer.from_string(app_key)
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

  api_object = json.dumps(api_object)
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
  success = True
  if success:
    jwt = {
      'iss': config.SERVICE_ACCOUNT_NAME,
      'aud': config.AUDIENCE,
      'typ': config.LOYALTY_WEB,
      'iat':  int(time.time()),
      'payload': {
        'webserviceResponse': {
          'result': 'approved',
          'message': 'Success.'
        },
        'loyaltyObjects': [],
        'offerObjects': []
      }
    }
    linking_id = request.params.get('linkingId')
    loyalty_object_id = linking_id if linking_id else config.LOYALTY_OBJECT_ID
    loyalty_object = loyalty.generate_loyalty_object(
        config.ISSUER_ID, config.LOYALTY_CLASS_ID, loyalty_object_id)
    jwt['payload']['loyaltyObjects'].append(loyalty_object)
  else:
    error_action = 'link' if request.params.get('linkingId') else 'signup'
    jwt = {
      'iss': config.SERVICE_ACCOUNT_NAME,
      'aud': config.AUDIENCE,
      'typ': config.LOYALTY_WEB,
      'iat':  int(time.time()),
      'payload': {
        'webserviceResponse': {
          'message': 'Sorry we can\'t complete this %s' % error_action,
          'result': 'rejected'
        }
      }
    }
  signer = crypt.Signer.from_string(app_key)
  signed_jwt = crypt.make_signed_jwt(signer, jwt)
  response = webapp2.Response(signed_jwt)
  response.content_type = 'Application/JWT'
  return response


application = webapp2.WSGIApplication([
    ('/', displayIndex),
    ('/jwt', handleJwt),
    ('/insert', handleInsert),
    ('/webservice', handleWebservice)
    ])
