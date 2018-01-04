import logging
import unittest

from mock import patch

# from testfixtures import LogCapture

logger = logging.getLogger(__name__)
from ocbot.external.route_slack import Slack

from tests.test_data import USER_INFO_HAS_REAL_NAME
from ocbot.keys import VERIFICATION_TOKEN, TOKEN
from tests.test_data import USER_INFO_HAS_NAME, USER_INFO_NO_NAME, MESSAGE


class SlackClientSetup(unittest.TestCase):
    # @patch('ocbot.external.route_slack.SlackClient')
    # def test_missing_required_params(self, mock_client):
    #     self.assertRaises(TypeError, Slack, verification_token=VERIFICATION_TOKEN)
    #     self.assertRaises(TypeError, Slack, api_key=TOKEN)
    #     self.assertRaises(TypeError, Slack)

    @patch('ocbot.external.route_slack.SlackClient')
    def test_setup(self, mock_client):
        # call setup function
        singleton = Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)
        # verify all values entered correctly
        self.assertEqual(singleton._api_key, TOKEN)
        self.assertEqual(singleton._verification_token, VERIFICATION_TOKEN)
        # test mock called.
        mock_client.assert_called_with(TOKEN)


class SlackTokenTests(unittest.TestCase):
    def test_bad_key(self):
        self.assertRaises(ValueError, Slack, api_key='false key', verification_token='very bad')

    def test_good_token(self):
        singleton = Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)
        response = singleton.auth_test()
        self.assertEqual(response['ok'], True)


# TODO convert this to testing things within external.route_slack
@patch('ocbot.external.route_slack.SlackClient.api_call')
class UserNameTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)

    def test_user_name_from_id_has_real_name(self, mock_client):
        """
        Asserts the user_name_from_id method returns the user's real name
        when it is present.
        """
        mock_client.return_value = USER_INFO_HAS_REAL_NAME
        real_name = self.client.user_name_from_id(USER_INFO_HAS_REAL_NAME['user']['id'])
        self.assertEquals(real_name, 'Episod')

    def test_user_name_from_id_real_name_blank_returns_name(self, mock_client):
        """
        Asserts the user_name_from_id method returns the user's name
        when their real name is absent but the username is present
        """
        mock_client.return_value = USER_INFO_HAS_NAME
        name = self.client.user_name_from_id(USER_INFO_HAS_NAME['user']['id'])
        self.assertEquals(name, 'Spengler')

    def test_user_name_from_id_no_name_return_new_member(self, mock_client):
        """
        Asserts the user_name_from_id method defaults to returning New Member
        when both real name and name are absent
        """
        mock_client.return_value = USER_INFO_NO_NAME
        name = self.client.user_name_from_id(USER_INFO_NO_NAME['user']['id'])
        self.assertEquals(name, 'New Member')


class BuildMessageTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Slack(api_key=TOKEN, verification_token=VERIFICATION_TOKEN)

    def test_build_message(self):
        """
        Asserts build_message function correctly formats message.
        """
        params = {
            'real_name': 'Bob'
        }
        message = self.client.build_message(MESSAGE, **params)
        self.assertEquals(message, MESSAGE.format(real_name='Bob'))

# # TODO Not currently using build_message
#
# @patch('ocbot.external.route_slack.Slack.user_name_from_id', return_value='bob')
# class NewMemberTestCase(unittest.TestCase):
#     @patch('utils.slack_utils.client.api_call', return_value={'ok': True, 'info': 'stuff goes here'})
#     def test_event_logged(self, mock_client, mock_username_from_id):
#         """
#         Asserts messages are being logged properly when new_member is called
#         """
#         with LogCapture() as capture:
#             message = MESSAGE.format(real_name="bob")
#             new_member(NEW_MEMBER)
#             capture.check(
#                 ('src.app.new_member', 'INFO', 'Recieved json event: {}'.format(NEW_MEMBER)),
#                 ('root', 'INFO', 'team_join message'),
#                 ('src.app.new_member', 'INFO', 'Built message: {}'.format(message)),
#                 ('src.app.new_member', 'INFO',
#                  'New Member Slack response: Response 1: {res} \nResponse2: {res}'.format(
#                      res={'ok': True, 'info': 'stuff goes here'}))
#             )
#
#     @patch('utils.slack_utils.client.')
#     def test_slack_client_called_with_correct_params(self, mock_client, mock_builder, mock_unfi):
#         """
#         Asserts new_member calls the client api with correct params for help menu.
#         """
#         with LogCapture() as capture:
#             new_member(NEW_MEMBER)
#         mock_client.api_call.assert_any_call('chat.postMessage',
#                                              channel=NEW_MEMBER['user']['id'],
#                                              as_user=True,
#                                              **HELP_MENU)
#
#     #
#     @patch('utils.slack_utils.client.api_call', return_value={'ok': False, 'info': 'stuff goes here'})
#     def test_slack_client_returns_error(self, mock_builder, mock_unfi, mock_client):
#         """
#         Asserts an ERROR is logged when messaging a new member fails
#         """
#         with LogCapture(level=logging.ERROR) as capture:
#             new_member(USER_INFO_HAS_REAL_NAME)
#             capture.check(
#                 ('src.app.new_member', 'ERROR',
#                  "FAILED -- Message to new member returned error: {res}\n{res}".format(
#                      res={'ok': False, 'info': 'stuff goes here'})))
