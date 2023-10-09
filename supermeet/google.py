from datetime import datetime, timedelta
from os import environ

import googleapiclient.discovery

from google.oauth2 import service_account

from . import CONFIG


class GoogleAPI:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            environ['APP_SECRETS'],
            scopes=[
                'https://www.googleapis.com/auth/calendar',
            ],
        ).with_subject(CONFIG['impersonate_user'])

        self.api = googleapiclient.discovery.build(
            'calendar', 'v3', credentials=credentials
        )

    def _date(self, dt):
        return dt.replace(tzinfo=None).isoformat('T') + 'Z'

    def get_room(self, room_id):
        return self.api.calendars().get(calendarId=room_id).execute()

    def get_room_events(self, room_id, start=None, until=None):
        if start is None:
            start = datetime.utcnow()

        if until is None:
            until = start + timedelta(days=14)

        all_events = []
        page_token = None
        while True:
            events = (
                self.api.events()
                .list(
                    calendarId=room_id,
                    pageToken=page_token,
                    timeMin=self._date(start),
                    timeMax=self._date(until),
                    singleEvents=True,
                )
                .execute()
            )
            page_token = events.get('nextPageToken')
            for event in events.get('items', []):
                if event.get('status') == 'confirmed':
                    room_accepted = False
                    if event.get('attendees'):
                        for attendee in event['attendees']:
                            if attendee.get('email') == room_id:
                                if attendee.get('responseStatus') == 'accepted':
                                    room_accepted = True
                                break
                    else:
                        room_accepted = True
                    if room_accepted:
                        all_events.append(event)
            if not page_token:
                break
        return all_events

    def create_event(self, room_id, title, start, end):
        return (
            self.api.events()
            .insert(
                calendarId=room_id,
                body={
                    'end': {
                        'dateTime': end,
                        'timeZone': CONFIG['timezone'],
                    },
                    'start': {
                        'dateTime': start,
                        'timeZone': CONFIG['timezone'],
                    },
                    'summary': title,
                },
            )
            .execute()
        )

    def patch_room_event_end_time(self, room_id, event_id, until):
        return (
            self.api.events()
            .patch(
                calendarId=room_id,
                eventId=event_id,
                body={
                    'end': {
                        'dateTime': until,
                        'timeZone': CONFIG['timezone'],
                    },
                },
            )
            .execute()
        )
