from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print(datetime.datetime.today()) -- Check :)
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    tomorrow = str(tomorrow)
    tomorrow = tomorrow.replace(" ", "T") + 'Z'

    #tomorrow = tomorrow.strftime('%Y-%m-%d-T10:00:00Z') # now is datetime.. not a string :(
    print('Tomorrow: ')
    print(tomorrow)
    print('\nGetting the upcoming 10 events ... Getting events of: \n' + now + '\n')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
		#timeMax="2018-03-21T10:00:00-06:00",
		timeMax=tomorrow,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    #print(events, "events")
	
	
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        # more = event['start'].get('
        # print(more)
        print(start, event['summary'])
        
		
		
        event_title = [event['summary']]
        # event['summary'] is the name of the event #
        print("event title: ", event['summary'])
		
        today_day = start[0:10]
        print("today day:", today_day)
        # today_day is the date for the current day #
		
        event_start = start[11:19]
        print("event start:", event_start)
		# event_start is the start time for the event #
        
        #return(event['summary'],event_start)
		#clear this statement & implement into section where it's called#

if __name__ == '__main__':
    main()