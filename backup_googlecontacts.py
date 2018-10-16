#!/usr/bin/env python3

from __future__ import print_function
from googleapiclient.discovery import build
import googleapiclient.errors
from httplib2 import Http
from oauth2client import file, client, tools
import time

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('people', 'v1', http=creds.authorize(Http()))

    # Call the People API
    nextpagetoken = "";
    retries = 10
    while retries:
        try:
            results = service.people().connections().list(
                pageToken=nextpagetoken,
                resourceName='people/me',
                pageSize=10,
                personFields='names,emailAddresses',
            ).execute()
        except googleapiclient.errors.HttpError as err:
            if err.resp.status == 429:
                # Too fast, back off
                time.sleep(1);
                retries -= 1
                continue
            else:
                raise
        connections = results.get('connections', [])
        nextpagetoken = results.get('nextPageToken', "")

        if not nextpagetoken:
            # No more pages,we are done
            break

        for person in connections:
            print(person)
            #names = person.get('names', [])
            #if names:
            #    name = names[0].get('displayName')
            #    print(name)

if __name__ == '__main__':
    main()
