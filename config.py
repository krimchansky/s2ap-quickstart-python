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

SERVICE_ACCOUNT_EMAIL_ADDRESS = '177146692044@developer.gserviceaccount.com'
ISSUER_ID = '2956054058108947698'
SERVICE_ACCOUNT_PRIVATE_KEY = 'wobs-privatekey.pem'
APPLICATION_NAME = 'YOUR_APP_NAME'
DISCOVERY_JSON = 'wobs-discovery.json'
LOYALTY_CLASS_ID = 'LoyaltyClassPython1'
LOYALTY_OBJECT_ID = 'LoyaltyObjectPython1'
OFFER_CLASS_ID = 'OfferClass'
OFFER_OBJECT_ID = 'OfferObject'
# List of origins for save to wallet button
ORIGINS = [
    'http://localhost:8080',
    'http://wobs-quickstart-python.appspot.com',
    'https://wobs-quickstart-python.appspot.com']

# Constants that are application agnostic.
AUDIENCE = 'google'
BAD_REQUEST = 400
LOYALTY_WEB = 'loyaltywebservice'
SAVE_TO_WALLET = 'savetowallet'
SCOPES = 'https://www.googleapis.com/auth/wallet_object.issuer'
