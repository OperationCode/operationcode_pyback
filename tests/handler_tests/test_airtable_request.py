import pytest
import pytest_mock
from ocbot.external.route_slack import Slack

from ocbot.pipeline.handlers.airtable_request_handler import NewAirtableRequestHandler
from tests.handler_tests.airtable_request_events import NEW_AIRTABLE_REQUEST_JSON, USER_ID_FROM_EMAIL_RESPONSE


@pytest.fixture
def new_request_handler():
    return NewAirtableRequestHandler(event_dict=NEW_AIRTABLE_REQUEST_JSON)


def test_email_pulled_from_request(new_request_handler: NewAirtableRequestHandler):
    assert new_request_handler._user_email == NEW_AIRTABLE_REQUEST_JSON['Email']


def test_event_dict_pulled_from_request(new_request_handler: NewAirtableRequestHandler):
    assert new_request_handler._event == NEW_AIRTABLE_REQUEST_JSON


def test_slack_queried_for_user_id_from_email(mocker: pytest_mock, new_request_handler: NewAirtableRequestHandler):
    mocker.patch.object(Slack, "user_id_from_email", return_value=USER_ID_FROM_EMAIL_RESPONSE)
    new_request_handler.api_calls()
    assert new_request_handler.api_dict['user'] == '<@AGF2354>'


def test_event_slack_user_used_when_user_id_query_fails(mocker: pytest_mock,
                                                        new_request_handler: NewAirtableRequestHandler):
    mocker.patch.object(Slack, "user_id_from_email", return_value={'ok': False})
    new_request_handler.api_calls()
    assert new_request_handler.api_dict['user'] == NEW_AIRTABLE_REQUEST_JSON['Slack User']
