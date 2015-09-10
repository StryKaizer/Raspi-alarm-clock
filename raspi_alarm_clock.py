import httplib2
import os
import time
from feed.date.rfc3339 import tf_from_timestamp  # also for the comparator
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
from ConfigParser import SafeConfigParser
from players import spop_play
from subprocess import call

settings = SafeConfigParser()
settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.cfg'))

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Raspi Volumio Alarm Clock'

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


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
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials


def main():
    """Fetches 10 upcoming events and plays spotify playlist if 1 occurs right now.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print 'Fetch the next 10 upcoming events'
    eventsResult = service.events().list(
        calendarId=settings.get('Calendar', 'GOOGLE_CALENDAR_ID'), timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        upcoming_event_start = time.strftime('%d-%m-%Y %H:%M', time.localtime(tf_from_timestamp(start)))
        print upcoming_event_start, event['summary']
        current_time = time.strftime('%d-%m-%Y %H:%M')
        if upcoming_event_start == current_time:

            # Initial setup fading functionality
            if settings.getboolean('Music', 'VOLUMIO_ENABLE_VOLUME_FADING'):
                current_volume = settings.getint('Music', 'VOLUMIO_INITIAL_VOLUME')
                end_volume = settings.getint('Music', 'VOLUMIO_ENDING_VOLUME')
                fade_time = settings.getint('Music', 'VOLUMIO_VOLUME_FADING_SECONDS')
                fading_steps = abs(end_volume - current_volume)
                step = 1
                if (end_volume < current_volume):
                    step = -1
                seconds_per_step = int(fade_time / fading_steps)

                # Set initial volume
                call(["mpc", "volume", str(current_volume)])

            # Start playing
            spop_play.play_music(settings)

            # Fade volume
            if settings.getboolean('Music', 'VOLUMIO_ENABLE_VOLUME_FADING'):
                while fading_steps > 0:
                    time.sleep(seconds_per_step)
                    current_volume += step
                    call(["mpc", "volume", str(current_volume)])
                    fading_steps -= 1


def list_calendars():
    """Fetches all calendars you have access to, and prints them, for debugging purpose.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print 'Fetching calendars'
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print calendar_list_entry['summary']
            print calendar_list_entry['id']
            print ""
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


if __name__ == '__main__':
    main()
