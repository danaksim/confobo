import datetime

from confobo.models.calendar import calendar


def get_schedule(date: str) -> str:
    """
    Return conference schedule for a given day

    :param date: date (string in %Y-%m-%d format) for which schedule has been requested

    :return: schedule for the date
    """
    day = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return calendar.events(day=day)
