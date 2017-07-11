from icalendar.cal import Event as ICalEvent

from confobo.config import DATETIME_FORMAT


class Event:
    def __init__(self, *args, **kwargs):

        id_ = description = dt_start = dt_end = location = None

        if args:
            if len(args) > 1 or type(args[0]) is not ICalEvent:
                raise TypeError()
            ical_event = args[0]
            id_ = ical_event.get('uid')
            description = ical_event.get('summary')
            dt_start = ical_event.get('dtstart').dt
            dt_end = ical_event.get('dtend').dt
            location = ical_event.get('location')

        id_ = kwargs.get('id') or id_
        description = kwargs.get('description') or description
        dt_start = kwargs.get('dt_start') or dt_start
        dt_end = kwargs.get('dt_end') or dt_end
        location = kwargs.get('location') or location

        if dt_start and dt_end and dt_start > dt_end:
            raise ValueError()

        self._id = id_
        self._description = description
        self.dt_start = dt_start
        self.dt_end = dt_end
        self.location = location

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def __repr__(self):
        return """
Event <{id}>

Description: {desc}
Location: {location}
Start: {start}
End: {end}
        """.format(id=self.id, desc=self.description, start=self.dt_start.strftime(DATETIME_FORMAT),
                   end=self.dt_end.strftime(DATETIME_FORMAT), location=self.location)
