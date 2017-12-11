from testfixtures import LogCapture
import unittest
import mock

from src import app
from .test_data import *


class EventHandlerTestCase(unittest.TestCase):

    @mock.patch('src.app.new_member')
    def test_event_handler_receives_team_join_calls_new_member(self, mock_new_member):
        app.event_handler(NEW_MEMBER)
        mock_new_member.assert_called_with(NEW_MEMBER)

    def test_event_handler_message_event_logs_event(self):
        with LogCapture() as capture:
            app.event_handler(MESSAGE_EVENT)
            capture.check(('src.app', 'INFO', 'Message event'))


@mock.patch('src.app.slack_client')
class UserNameTestCase(unittest.TestCase):

    def test_user_name_from_id_has_real_name(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_HAS_REAL_NAME
        real_name = app.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
        self.assertEquals(real_name, 'Episod')

    def test_user_name_from_id_real_name_blank_returns_name(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_HAS_NAME
        name = app.user_name_from_id(USER_INFO_HAS_NAME['user']['id'])
        self.assertEquals(name, 'Spengler')

    def test_user_name_from_id_no_name_return_new_member(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_NO_NAME
        name = app.user_name_from_id(USER_INFO_NO_NAME['user']['id'])
        self.assertEquals(name, 'New Member')


@mock.patch('src.app.user_name_from_id', return_value='bob')
@mock.patch('src.app.build_message', return_value=MESSAGE)
@mock.patch('src.app.slack_client')
class NewMemberTestCase(unittest.TestCase):

    def test_event_logged(self, mock_client, mock_builder, mock_username_from_id):
        with LogCapture() as capture:
            app.new_member(NEW_MEMBER)
            capture.check(
                ('src.app.new_member', 'INFO', 'Recieved json event: {}'.format(NEW_MEMBER)),
                ('root', 'INFO', 'team_join message'),
                ('src.app.new_member', 'INFO', 'Built message: {}'.format(NEW_MEMBER)),
                ('src.app.new_member', 'INFO', 'New Member Slack response: {}'.format(NEW_MEMBER))
            )

    def test_slack_client_called_with_correct_params(self, mock_client, mock_builder, mock_unfi):
        app.new_member(NEW_MEMBER)
        mock_client.api_call.assert_called_with('chat.postMessage',
                                                channel=NEW_MEMBER['user']['id'],
                                                text=MESSAGE, as_user=True)
