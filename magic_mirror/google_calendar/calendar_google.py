from __future__ import print_function

import json

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main(calendar_events_path, credentials):
    CLIENT_FILE = credentials
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly",
              "https://www.googleapis.com/auth/calendar.events.readonly"]

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service_calendar = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service_calendar.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        print(events)
        event_date_summary = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            single_event = start, event['summary']
            event_date_summary.append(single_event)
        # with open(calendar_path, "w") as calendar:
        #     json.dump(events, calendar, indent=4)
        with open(calendar_events_path, "w") as calendar:
            json.dump(event_date_summary, calendar, indent=4)

    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    # calendar_path = "../static/calendar_ev.json"
    calendar_events_path = "../static/calendar_events.json"
    credentials = "credentials.json"
    main(calendar_events_path, credentials)