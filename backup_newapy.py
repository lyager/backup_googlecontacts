#!/usr/bin/env python3

import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run_flow

FLOW = OAuth2WebServerFlow(
    client_id='100650188922-pga1eqnfduf66b4ntbd8o38o4mlu8721.apps.googleusercontent.com',
    client_secret='rRatT2kJTZ1jChUW30DRGXzx',
    scope='https://www.googleapis.com/auth/contacts.readonly',
    user_agent='contactbakcup/1.0')

storage = Storage('info.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run_flow(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and
# authorize it with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. To get an API key for
# your application, visit the Google API Console
# and look at your application's credentials page.
people_service = build(serviceName='people', version='v1', http=http)
