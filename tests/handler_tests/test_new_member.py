import pytest
import pytest_mock

from ocbot.external.route_slack import Slack
from tests.handler_tests.events import *
from ocbot.pipeline.handlers.newmember import NewMemberHandler
from ocbot.pipeline.handlers.newmember import base_resources
from ocbot.pipeline.utils import needs_greet_button

VERIFICATION_TOKEN = 'fake_token'
TOKEN = 'fake_token'


@pytest.fixture
def slack(mocker: pytest_mock.mocker):
    """ Returns an instance of a correctly configured client """

    mocker.patch('ocbot.external.route_slack.Slack.user_name_from_id', return_value='spengler')
    mocker.patch('ocbot.external.route_slack.Slack.api_call', return_value={'ok': True})
    mocker.patch('ocbot.external.route_slack.Slack._default', return_value={'ok': True})
    return Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)


@pytest.fixture
def new_member_handler():
    return NewMemberHandler(event_dict=NEW_MEMBER)


@pytest.fixture
def needs_greet_mocker():
    return needs_greet_button()


## instantiation tests ##
def test_build_not_implicitly_called(mocker, new_member_handler):
    build_spy = mocker.spy(new_member_handler, 'build_responses')
    assert not build_spy.called


##  built_templates tests ##
## db response processing
def test_process_db_called(mocker, slack, new_member_handler):
    # test called
    new_member_handler.api_dict['real_name'] = slack.user_name_from_id()
    process_db_spy = mocker.spy(new_member_handler, "process_db_response")
    new_member_handler.build_templates()
    assert process_db_spy.called


def test_process_db_results_no_db_dict(new_member_handler):
    default_resources = new_member_handler.process_db_response()
    assert default_resources == base_resources


## main greet text processing
def test_main_greet_called(mocker, slack, new_member_handler):
    new_member_handler.api_dict['real_name'] = slack.user_name_from_id()
    process_db_spy = mocker.spy(new_member_handler, "process_db_response")
    new_member_handler.build_templates()
    assert process_db_spy.called


def test_main_greet_correct_message(slack, new_member_handler):
    new_member_handler.api_dict['real_name'] = slack.user_name_from_id()
    new_member_handler.build_templates()
    assert new_member_handler.text_dict['message'] == CORRECT_NAME_GREET
    assert new_member_handler.text_dict['message'] != UNPROCESSED_MAIN_GREET


## joined text processing
def test_joined_text_called(mocker, slack, new_member_handler):
    new_member_handler.api_dict['real_name'] = slack.user_name_from_id()
    new_member_handler.build_templates()
    assert new_member_handler.text_dict['community'] == CORRECT_JOINED_MESSAGE.format(new_member_handler.user_id)


def test_joined_text_correct_message(new_member_handler, needs_greet_mocker):
    assert needs_greet_mocker == CORRECT_GREET_BUTTON


## need greet button processing
def test_greet_button_called(mocker, slack, new_member_handler):
    new_member_handler.api_dict['real_name'] = slack.user_name_from_id()
    new_member_handler.build_templates()
    mocker.patch('ocbot.pipeline.utils.needs_greet_button')


def test_greet_button_correct_message(needs_greet_mocker):
    assert needs_greet_mocker == CORRECT_GREET_BUTTON


##  build_responses tests ##
def test_dict_vals_extracted(mocker, slack, new_member_handler):
    new_member_handler.event_route()
    include_resp_spy = mocker.spy(new_member_handler, 'include_resp')
    new_member_handler.build_responses()
    assert include_resp_spy.call_count == 4
