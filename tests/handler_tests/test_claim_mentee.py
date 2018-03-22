import pytest
import pytest_mock
from ocbot.external.route_airtable import AirTableBuilder
from ocbot.pipeline.handlers.claim_mentee import MenteeClaimHandler
from tests.handler_tests.airtable_request_events import CLAIM_MENTEE_EVENT, INVALID_MENTOR_ID_TEXT, \
    RESET_MENTEE_CLAIM_EVENT, RESET_MENTEE_ATTACHMENT, SLACK_USER_INFO

FAKE_RECORD_ID = 'rec123'

AIRTABLE_MENTOR_ID_CALL = 'ocbot.external.route_airtable.Airtable.mentor_id_from_slack_email'
SLACK_INFO_CALL = 'ocbot.external.route_slack.Slack.user_info_from_id'
SLACK_AUTH_TEST = 'ocbot.external.route_slack.Slack.auth_test'

@pytest.fixture
def claim_handler():
    return MenteeClaimHandler(event_dict=CLAIM_MENTEE_EVENT)


@pytest.fixture
def reset_handler():
    return MenteeClaimHandler(event_dict=RESET_MENTEE_CLAIM_EVENT)


def test_mentee_claim_handler_initializes_without_error(claim_handler: MenteeClaimHandler):
    pass


def test_has_correct_user_id(claim_handler: MenteeClaimHandler):
    assert claim_handler._user_id == CLAIM_MENTEE_EVENT['user']['id']


def test_has_correct_user_name(claim_handler: MenteeClaimHandler):
    assert claim_handler._user_name == CLAIM_MENTEE_EVENT['user']['name']


def test_correctly_stores_event(claim_handler: MenteeClaimHandler):
    assert claim_handler._event == CLAIM_MENTEE_EVENT


def test_has_correct_click_type_when_claim(claim_handler: MenteeClaimHandler):
    assert claim_handler.click_type == CLAIM_MENTEE_EVENT['actions'][0]['value']


def test_has_correct_record_id(claim_handler: MenteeClaimHandler):
    assert claim_handler._record_id == CLAIM_MENTEE_EVENT['actions'][0]['name']


def test_calls_airtable_for_mentor_id(mocker: pytest_mock, claim_handler: MenteeClaimHandler):
    mocker.patch(SLACK_AUTH_TEST)
    mocker.patch(SLACK_INFO_CALL, return_value=SLACK_USER_INFO)
    mock = mocker.patch(AIRTABLE_MENTOR_ID_CALL, return_value=FAKE_RECORD_ID)


    claim_handler.api_calls()
    assert mock.called
    assert claim_handler.api_dict['mentor_id'] == FAKE_RECORD_ID


def test_mentee_claimed_attachment_called_when_has_valid_mentor_id(mocker: pytest_mock,
                                                                   claim_handler: MenteeClaimHandler):
    claim_handler.api_dict['mentor_id'] = FAKE_RECORD_ID
    spy = mocker.spy(claim_handler, 'mentee_claimed_attachments')
    claim_handler.build_templates()
    assert spy.called


def test_correct_attachment_when_invalid_mentor_id(mocker: pytest_mock,
                                                   claim_handler: MenteeClaimHandler):
    claim_handler.api_dict['mentor_id'] = ''
    spy = mocker.spy(claim_handler, 'mentee_unclaimed_attachment')
    claim_handler.build_templates()
    assert spy.called
    assert claim_handler.text_dict['message']['attachments'][0]['text'] == INVALID_MENTOR_ID_TEXT


def test_has_correct_click_type_when_reset(reset_handler: MenteeClaimHandler):
    assert reset_handler.click_type == RESET_MENTEE_CLAIM_EVENT['actions'][0]['value']


def test_has_correct_attachment_when_reset(mocker: pytest_mock, reset_handler: MenteeClaimHandler):
    mocker.patch.object(reset_handler, 'now', return_value=11111)
    reset_handler.api_dict['mentor_id'] = FAKE_RECORD_ID
    reset_handler.build_templates()
    assert reset_handler.text_dict['message']['attachments'] == RESET_MENTEE_ATTACHMENT


def test_build_correct_response_when_mentee_claimed(mocker: pytest_mock, claim_handler: MenteeClaimHandler):
    claim_handler.api_dict['mentor_id'] = FAKE_RECORD_ID
    claim_handler.text_dict['message'] = {}
    record = CLAIM_MENTEE_EVENT['actions'][0]['name']
    correct_airtable_response = AirTableBuilder.claim_mentee(record, FAKE_RECORD_ID)

    claim_handler.build_responses()

    assert correct_airtable_response in claim_handler.response
