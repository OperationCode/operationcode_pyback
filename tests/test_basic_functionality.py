import unittest
import mock

from testfixtures import LogCapture

from src import app
from .test_data import *


class FakeClient:
    def __init__(self):
        self.rtm_messages = []

    def rtm_send_message(self, channel, message, attachments=None):
        self.rtm_messages.append((channel, message))


class EventHandlerTestCase(unittest.TestCase):

    @mock.patch('src.app.new_member')
    def test_event_handler_receives_team_join_calls_new_member(self, mock):
        app.event_handler(NEW_MEMBER)
        mock.assert_called_with(NEW_MEMBER)

    def test_event_handler_message_event_logs_event(self):
        with LogCapture() as capture:
            app.event_handler(MESSAGE_EVENT)
            capture.check(('src.app', 'INFO', 'Message event'))


class UserNameTestCase(unittest.TestCase):

    @mock.patch('src.app.slack_client')
    def test_user_name_from_id_has_real_name(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_HAS_REAL_NAME
        real_name = app.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
        self.assertEquals(real_name, 'Episod')

    @mock.patch('src.app.slack_client')
    def test_user_name_from_id_real_name_blank_returns_name(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_HAS_NAME
        name = app.user_name_from_id(USER_INFO_HAS_NAME['user']['id'])
        self.assertEquals(name, 'Spengler')

    @mock.patch('src.app.slack_client')
    def test_user_name_from_id_real_name_blank_returns_name(self, mock_client):
        mock_client.api_call.return_value = USER_INFO_HAS_NAME
        name = app.user_name_from_id(USER_INFO_HAS_NAME['user']['id'])
        self.assertEquals(name, 'Spengler')
