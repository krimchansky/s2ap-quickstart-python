Python Quick Start Sample for Wallet Object API Copyright (C) 2013 Google Inc.

wallet-objects-quickstart-Python
==============================

Basic Python implementation of the Google Wallet for Wallet Objects API.

This sample aims to provide a straight forward example of how to integrate the basic components of the Wallet Objects API.

### Setup

To setup the sample, edit config.py.

*  If you don't already have a Google contact, submit the [Sign up for  Wallet Objects API access form](https://support.google.com/wallet/objects/contact/WOB_interest?rd=1). Google will respond to qualified merchants with instructions on how to set up merchant credentials. Replace ISSUER_ID in config.php with your Merchant Id.
* Create an API project in the [Google API Console](https://code.google.com/apis/console/) then select the API Access tab in your API project, and click on Create an OAuth 2.0 client ID button. Select service account option from the list, Download the generated private key and save it in your application folder.
* Convert the private key from pkcs12 to RSA. For example you can use the following command in linux - 'openssl pkcs12 -in pkey.p12 -nodes -nocerts > privatekey.pem'
* Also enable Wallet Objects API in services tab.
* Replace CLIENT_ID, SERVICE_ACCOUNT_NAME, KEY_FILE and ORIGINS with your OAuth client Id, service account email address, private key file path and application origin url in config.py file.

### Google appengine.

To run application on google appengine requires [Google App Engine SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)

1. Create a new application at your [appengine account](https://appengine.google.com).
2. Change application name in app.yaml file.

### Local dev.

Run dev_appserver.py to start the localhost. Add 'http://localhost:PORT_NUM' to the list named ORIGINS in config.py where PORT_NUM is the port number of your local server (default - 8080).

The app showcases several aspects of the API

* Creation of Wallet Classes and Objects
* Save to Wallet insertion of Classes and Objects
* Webservice API

## Creation of Wallet Classes and Objects
Example code for creation of Classes and Objects can be found in the files named offer.py and loyalty.py. Each vertical is present in it's own file.

## Save to Wallet insertion of Classes and Objects
Save to Wallet is handled on both the client and server side. index.html is the landing page which then includes app.js. App.js makes a request to the /jwt to generate vertical specific JWTs. Once all of the JWTs are generated, app.js inserts the appropriate g:wallet tags and the Save to Wallet JS.

## Webservice API
The Webservice API handler is the handleWebService function in main.py. This function handles Webservice requests, generates Loyalty Objects converts them to JWTs and responds with the JWT. You can configure your discoverable to point to the URL handled by the function.