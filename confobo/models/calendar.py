import os
from icalendar import Calendar as ICalendar

from .event import Event
from confobo.config import PROJECT_ROOT

SAMPLE_FILE = os.path.join(PROJECT_ROOT, 'data/calendar.ics')


class Calendar:
    def __init__(self, path_to_ics: str):
        with open(path_to_ics, 'rb') as file:
            cal = ICalendar.from_ical(file.read())
        self._ical = cal
        self._events = []
        for component in self._ical.walk(name='VEVENT'):
            e = Event(component)
            self._events.append(e)

    def __iter__(self):
        for e in self._events:
            yield e

    def events(self, **kwargs) -> list:
        if not kwargs:
            return self._events
        events = []
        if kwargs.get('day'):
            day = kwargs.get('day')
            events.extend(e for e in self._events if e.dt_start.date() == day)
        return events

calendar = Calendar(SAMPLE_FILE)
