import logging
import pytest

from ocbot.external.route_slack import Slack
import pytest_mock
from tests.test_data import USER_INFO_HAS_REAL_NAME
from tests.test_data import USER_INFO_HAS_NAME, USER_INFO_NO_NAME, MESSAGE


logger = logging.getLogger(__name__)
VERIFICATION_TOKEN = 'fake_token'
TOKEN = 'fake_token'


@pytest.fixture
def slack(mocker: pytest_mock.mocker):
    """ Returns an instance of a correctly configured client """

    mocker.patch('ocbot.external.route_slack.Slack.api_call', return_value={'ok': True})
    return Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)


# Username tests
def test_user_name_from_id_has_real_name(mocker, slack):
    """
    Asserts the user_name_from_id method returns the user's real name
    when it is present.
    """
    mocker.patch.object(slack, 'api_call', return_value=USER_INFO_HAS_REAL_NAME)
    real_name = slack.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
    assert real_name == 'Episod'


def test_user_name_from_id_real_name_blank_returns_name(mocker, slack):
    """
    Asserts the user_name_from_id method returns the user's name
    when their real name is absent but the username is present
    """

    mocker.patch.object(slack, 'api_call', return_value=USER_INFO_HAS_NAME)
    real_name = slack.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
    assert real_name == 'Spengler'


def test_user_name_from_id_no_name_return_new_member(mocker, slack):
    """
    Asserts the user_name_from_id method defaults to returning New Member
    when both real name and name are absent
    """
    mocker.patch.object(slack, 'api_call', return_value=USER_INFO_NO_NAME)
    real_name = slack.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
    assert real_name == 'New Member'


# Build message test
def test_build_message(slack):
    """
    Asserts build_message function correctly formats message.
    """
    params = {
        'real_name': 'Bob'
    }
    message = slack.build_message(MESSAGE, **params)
    assert message == MESSAGE.format(real_name='Bob')
