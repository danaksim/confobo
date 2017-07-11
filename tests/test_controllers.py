import pytest
from unittest.mock import Mock

from confobo.models.calendar import calendar
from confobo.models.event import Event
from confobo.models.user import User
from confobo import controllers
from confobo import persistence


@pytest.fixture(scope="module")
def fixture_user():
    return User(1)


@pytest.fixture(scope="module")
def fixture_event():
    return Event(id=1)


def test_vote(fixture_user, fixture_event):
    persistence.voting.save_vote = Mock(return_value=True)
    vote_acceptable = 4
    vote_unacceptable = 6

    assert controllers.voting.vote(fixture_user, vote_acceptable, fixture_event) is True
    with pytest.raises(controllers.voting.BadVoteValueError):
        controllers.voting.vote(fixture_user, vote_unacceptable, fixture_event)


def test_remove_subs(fixture_user):
    persistence.subscriptions.remove_all = Mock(return_value=True)

    assert controllers.subscriptions.remove_all(fixture_user) is True


def test_schedule():
    events = calendar.events()
    assert len(events) == 3
    wed_events = controllers.schedule.get_schedule('2017-07-12')
    assert len(wed_events) == 2
    assert wed_events[0].description == 'Event 1'
    assert wed_events[0].location == 'Room 404'
