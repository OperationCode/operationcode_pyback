from testfixtures import LogCapture
import unittest
import mock
import logging

from src import app
from src.messages import HELP_MENU
from .test_data import *


class EventHandlerTestCase(unittest.TestCase):

    @mock.patch('src.app.new_member')
    def test_event_handler_receives_team_join_calls_new_member(self, mock_new_member):
        """
        Asserts event_handler correctly passes the event to the new_member function
        when event type is 'team_join'
        """
        app.event_handler(NEW_MEMBER)
        mock_new_member.assert_called_with(NEW_MEMBER)

    #   All events logging currently disabled
    #
    # def test_event_handler_message_event_logs_event(self):
    #     """
    #     Asserts event handler correctly logs message events.
    #     Will be removed eventually...
    #     """
    #     with LogCapture() as capture:
    #         app.event_handler(MESSAGE_EVENT)
    #         capture.check(
    #             ('src.app.all_events',
    #              'INFO',
    #              "{'type': 'message', 'channel': 'C8DA69KM4', 'user': 'U8DG4B3EK', 'text': "
    #              "'.', 'ts': '1513003671.000412', 'source_team': 'T8CJ90MQV', 'team': "
    #              "'T8CJ90MQV'}"),
    #             ('src.app', 'INFO', 'Message event')
    #         )


@mock.patch('src.app.slack_client')
class UserNameTestCase(unittest.TestCase):

    def test_user_name_from_id_has_real_name(self, mock_client):
        """
        Asserts the user_name_from_id method returns the user's real name
        when it is present.
        """
        mock_client.api_call.return_value = USER_INFO_HAS_REAL_NAME
        real_name = app.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
        self.assertEquals(real_name, 'Episod')

    def test_user_name_from_id_real_name_blank_returns_name(self, mock_client):
        """
        Asserts the user_name_from_id method returns the user's name
        when their real name is absent but the username is present
        """
        mock_client.api_call.return_value = USER_INFO_HAS_NAME
        name = app.user_name_from_id(USER_INFO_HAS_NAME['user']['id'])
        self.assertEquals(name, 'Spengler')

    def test_user_name_from_id_no_name_return_new_member(self, mock_client):
        """
        Asserts the user_name_from_id method defaults to returning New Member
        when both real name and name are absent
        """
        mock_client.api_call.return_value = USER_INFO_NO_NAME
        name = app.user_name_from_id(USER_INFO_NO_NAME['user']['id'])
        self.assertEquals(name, 'New Member')


@mock.patch('src.app.user_name_from_id', return_value='bob')
@mock.patch('src.app.build_message', return_value=MESSAGE)
class NewMemberTestCase(unittest.TestCase):

    @mock.patch('src.app.slack_client.api_call', return_value={'ok': True, 'info': 'stuff goes here'})
    def test_event_logged(self, mock_client, mock_builder, mock_username_from_id):
        """
        Asserts messages are being logged properly when new_member is called
        """
        with LogCapture() as capture:
            message = MESSAGE.format(real_name="bob")
            app.new_member(NEW_MEMBER)
            capture.check(
                ('src.app.new_member', 'INFO', 'Recieved json event: {}'.format(NEW_MEMBER)),
                ('root', 'INFO', 'team_join message'),
                ('src.app.new_member', 'INFO', 'Built message: {}'.format(message)),
                ('src.app.new_member', 'INFO',
                 'New Member Slack response: Response 1: {res} \nResponse2: {res}'.format(
                     res={'ok': True, 'info': 'stuff goes here'}))
            )

    @mock.patch('src.app.slack_client')
    def test_slack_client_called_with_correct_params(self, mock_client, mock_builder, mock_unfi):
        """
        Asserts new_member calls the client api with correct params for help menu.
        """
        with LogCapture() as capture:
            app.new_member(NEW_MEMBER)
        mock_client.api_call.assert_any_call('chat.postMessage',
                                             channel=NEW_MEMBER['user']['id'],
                                             **HELP_MENU)

    #
    @mock.patch('src.app.slack_client.api_call', return_value={'ok': False, 'info': 'stuff goes here'})
    def test_slack_client_returns_error(self, mock_builder, mock_unfi, mock_client):
        """
        Asserts an ERROR is logged when messaging a new member fails
        """
        with LogCapture(level=logging.ERROR) as capture:
            app.new_member(USER_INFO_HAS_REAL_NAME)
            capture.check(
                ('src.app.new_member', 'ERROR',
                 "FAILED -- Message to new member returned error: {'ok': False, 'info': 'stuff goes here'}"))


class BuildMessageTestCase(unittest.TestCase):

    def test_build_message(self):
        """
        Asserts build_message function correctly formats message.
        """
        message = app.build_message(MESSAGE, real_name='Bob')
        self.assertEquals(message, MESSAGE.format(real_name='Bob'))
