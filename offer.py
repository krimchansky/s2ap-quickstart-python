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

def generate_offer_class(issuer_id, class_id):
  offer_class = {
      'kind': 'walletobjects#offerClass',
      'id': '%s.%s' % (issuer_id, class_id),
      'version': '1',
      'issuerName': 'Baconrista Coffee',
      'issuerData': {
          'kind': 'walletobjects#typedValue'
      },
      'renderSpecs': [{
          'viewName': 'g_list',
          'templateFamily': '1.offer1_list'
          },{
          'viewName': 'g_expanded',
          'templateFamily': '1.offer1_expanded'
      }],
      'allowMultipleUsersPerObject': True,
      'homepageUri': {
          'kind': 'walletobjects#uri',
          'uri': 'http://www.google.com/landing/chrome/ugc/chrome-icon.jpg',
          'description': 'Website'
      },
      'locations': [{
          'kind': 'walletobjects#latLongPoint',
          'latitude': 37.442087,
          'longitude': -122.161446
          },{
          'kind': 'walletobjects#latLongPoint',
          'latitude': 37.429379,
          'longitude': -122.12272999999999
          },{
          'kind': 'walletobjects#latLongPoint',
          'latitude': 37.333646,
          'longitude': -121.884853
      }],
      'reviewStatus': 'underReview',
      'review': {
          'comments': 'Real auto approval by system'
      },
      'title': '20% off one cup of cofee',
      'redemptionChannel': 'both',
      'provider': 'Baconrista Deals',
      'titleImage': {
          'kind': 'walletobjects#image',
          'sourceUri': {
              'kind': 'walletobjects#uri',
              'uri': 'http://3.bp.blogspot.com/-AvC1agljv9Y/TirbDXOBIPI/' +
                     'AAAAAAAACK0/hR2gs5h2H6A/s1600/Bacon%2BWallpaper.png'
          }
      },
      'details': '20% off one cup of coffee at all Baconristas.'
    }
  return offer_class

def generate_offer_object(issuer_id, class_id, object_id):
  offer_object = {
      'kind': 'walletobjects#offerObject',
      'classId': '%s.%s' % (issuer_id, class_id),
      'id': '%s.%s' % (issuer_id, object_id),
      'version': '1',
      'state': 'active',
      'issuerData': {
          'kind': 'walletobjects#typedValue'
      },
      'barcode': {
          'kind': 'walletobjects#barcode',
          'type': 'upcA',
          'value': '123456789012',
          'label': 'User Id',
          'alternateText': '12345'
      }
  }
  return offer_object
