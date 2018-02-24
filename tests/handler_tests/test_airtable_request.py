import pytest
import pytest_mock
from ocbot.external.route_slack import Slack, SlackBuilder
from ocbot.external.route_airtable import AirTableBuilder
from config.configs import configs

from ocbot.pipeline.handlers.airtable_request_handler import NewAirtableRequestHandler
from tests.handler_tests.airtable_request_events import NEW_AIRTABLE_REQUEST_JSON, USER_ID_FROM_EMAIL_RESPONSE, \
    TEXT_DICT_MESSAGE, TEXT_DICT_DETAILS

MENTORS_INTERNAL_CHANNEL = configs['MENTORS_INTERNAL_CHANNEL']
SLACK_USER_ID = '<@AGF2354>'


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
    assert new_request_handler.api_dict['user'] == SLACK_USER_ID


def test_event_slack_user_used_when_user_id_query_fails(mocker: pytest_mock,
                                                        new_request_handler: NewAirtableRequestHandler):
    mocker.patch.object(Slack, "user_id_from_email", return_value={'ok': False})
    new_request_handler.api_calls()
    assert new_request_handler.api_dict['user'] == NEW_AIRTABLE_REQUEST_JSON['Slack User']


def test_airtable_builder_called_to_translate_service(mocker: pytest_mock,
                                                      new_request_handler: NewAirtableRequestHandler):
    airtable_spy = mocker.spy(AirTableBuilder, "record_to_service")
    new_request_handler.api_dict['user'] = SLACK_USER_ID

    new_request_handler.build_templates()

    assert airtable_spy.call_count == 1


def test_text_dict_populated(new_request_handler: NewAirtableRequestHandler):
    new_request_handler.api_dict['user'] = SLACK_USER_ID

    new_request_handler.build_templates()

    assert new_request_handler.text_dict['message']
    assert new_request_handler.text_dict['details']


def test_correct_response_added(new_request_handler: NewAirtableRequestHandler):
    new_request_handler.text_dict['message'] = TEXT_DICT_MESSAGE
    new_request_handler.text_dict['details'] = TEXT_DICT_DETAILS
    correct_response = SlackBuilder.mentor_request(MENTORS_INTERNAL_CHANNEL,
                                                   details=TEXT_DICT_DETAILS,
                                                   text=TEXT_DICT_MESSAGE)

    new_request_handler.build_responses()

    assert correct_response in new_request_handler.response
