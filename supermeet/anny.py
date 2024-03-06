from datetime import datetime, timedelta
from os import environ

from requests import Session

from . import CONFIG


class AnnyAPI:
    def __init__(self):
        self.session = Session()
        self.session.headers = {
            'Authorization': f'Bearer {CONFIG["anny_api_key"]}',
        }

    def __get(self, api_endpoint):
        r = self.session.get(f'https://b.anny.co{api_endpoint}')
        r.raise_for_status()
        return r.json()

    def get_events(self, start=None, until=None):
        if start is None:
            start = datetime.utcnow() - timedelta(days=1)

        if until is None:
            until = start + timedelta(days=14)

        all_events = []

        events = self.__get('/api/v1/bookings?include=resource&filter[end_date]={end}&filter[start_date]={start}'.format(
            start=start.isoformat()[:19],
            end=until.isoformat()[:19],
        ))
        for booking in events['data']:
            if booking['attributes']['status'] in ('accepted', 'requested', 'reserved'):
                all_events.append(booking)
        return all_events
