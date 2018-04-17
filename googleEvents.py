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
	credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

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

def main(): #day_wanted
	"""Shows basic usage of the Google Calendar API.
	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	##if (day_wanted != none): #day_wanted is not null
	##	now = day_wanted
	##else:
		#now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	morning = str(now)
	morning = morning[0:11]
	#utc is 5 hours in the future.
	morning = (morning + '01:00:00.00Z')
	#morning is now at 6AM (central)
	print('Morning: ')
	print(morning)
	
	night = morning[:11] + '23:59' + morning[16:]
	#text = text[:8] + "slept" + text[11:]
	#tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
	#tomorrow = str(tomorrow)
	#tomorrow = tomorrow.replace(" ", "T") + 'Z'

	#tomorrow = tomorrow.strftime('%Y-%m-%d-T10:00:00Z') # now is datetime.. not a string :(
	print('Night: ')
	print(night)
	print('\nGetting the upcoming 10 events ... Getting events of: \n' + morning + '\n')
	eventsResult = service.events().list(calendarId='primary', timeMin=morning, maxResults=10, singleEvents=True,timeMax=night,orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	#print(events, "events")
	
	
	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		end = event['end'].get('dateTime',event['end'].get('date'))
		
		
		print('\n', start, event['summary'])

		print('\n end:', end, '\n')
		
		
		
		event_title = [event['summary']]
		# event['summary'] is the name of the event #
		print("event title:", event['summary'])
		
		today_day = start[0:10]
		print("today day:", today_day)
		# today_day is the date for the current day #
		
		time_start = start[11:19]
		print("time start:", time_start)
		# event_start is the start time for the event #

		time_end = end[11:19]
		print("time end:", time_end)
	
		try:
			color_ID = event['colorId']
			print("ColorId:", color_ID)
		except:
			color_ID = 5
			print("ColorId:", color_ID)
		
		#return(event['summary'],event_start)
		#clear this statement & implement into section where it's called#

if __name__ == '__main__':
	main()