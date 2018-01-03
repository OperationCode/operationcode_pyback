import logging
from functools import partial
from typing import List
from uuid import UUID

from slackclient import SlackClient
from ..keys import VERIFICATION_TOKEN, TOKEN

from ocbot.external.utils import ResponseContainer

logger = logging.getLogger(__name__)


# @verify_module_variable(['VERIFICATION_TOKEN', 'API_KEY'], Slack, 'slack')
class SlackBuilder:
    """
    user_id and flattened dict get passed
    """

    # TODO determine if need as_user
    @staticmethod
    def message(channel, **message_payload):
        return ResponseContainer(route='Slack',
                                 method='chat.postMessage',
                                 payload=dict(channel=channel,
                                              as_user=True,  # optional?
                                              **message_payload))

    @staticmethod
    def update(**message_payload):
        return ResponseContainer(route='Slack',
                                 method='chat.update',
                                 payload=dict(**message_payload))


class Slack:
    # Store the instance
    __shared_state = {}
    _api_key = None
    _verification_token = None
    _client = None

    def __init__(self, *, api_key=None, verification_token=None):
        self.__dict__ = self.__shared_state
        self._api_key = api_key or TOKEN
        self._verification_token = verification_token or VERIFICATION_TOKEN
        self._client = SlackClient(self._api_key)
        self.auth_test()

    def __getattr__(self, name):
        """
        called when getattr(self, name) is not found
        :return:
        :rtype:
        """
        return partial(self._default, name)

    def _default(self, method, payload):
        print(f'default found.... {method}, {payload}')
        res = self._client.api_call(method, **payload)
        print('API call result: ', res)
        return res

    # TODO add exception handling for the cases
    def user_name_from_id(self, user_id: str) -> str:
        """
        Queries the Slack workspace for t   he users real name
        to personalize messages.  Prioritizes real_name -> name -> 'New Member'
        :param user_id:
        """
        response = self._client.api_call('users.info', user=user_id)
        print(f'response: {response}')
        try:
            if response['user']['real_name']:
                return response['user']['real_name'].title()
            elif response['user']['name']:
                return response['user']['name'].title()
        except KeyError as error:
            logging.exception(error)
        else:
            return 'New Member'

    def auth_test(self):
        response = self._client.api_call('auth.test')
        if not response['ok']:
            if response['error'] == 'invalid auth':
                raise ValueError('Invalid auth recieved')
            raise ValueError(f"Auth error recieved: {response['error']}")
        return response

    def is_slack_success(self, response_list: List[ResponseContainer]) -> bool:
        for item in response_list:
            try:
                yield self._slack_client.api_call(item.call_method, **item.response)

            except Exception as response:
                yield logging.exception(response, UUID)

    def print_channels(self):
        channels = self._client.api_call("channels.list")
        if channels.get('ok'):

            for channel in channels['channels']:
                print(channel['name'] + " (" + channel['id'] + ")")
            print('-----')
        else:
            print("Unable to authenticate.")

    def get_bot_id(self, bot_name):
        response = self.client.api_call('users.list')
        if response.get('ok'):
            # retrieve all users so we can find our bot
            users = response.get('members')
            for user in users:
                if 'name' in user and user.get('name') is bot_name:
                    print(f"Bot ID for {user['name']} is {user.get('id')}")
        else:
            print(f"Could not find bot user with the name {bot_name}")

    def join_channels(self, channel: str) -> str:
        """
        Utility function for joining channels.  Move to utils?
        """
        return self.client.api_call('channels.join', name=channel)

    def build_message(self, message_template: str, **kwargs: dict) -> str:
        return message_template.format(**kwargs)

# def get_response_type(response_data):
#     return response_data['actions'][0]['value']
#
# def make_base_params(data, text_value, ):
#     return {'text': text_value,
#             'channel': data['channel']['id'],
#             'ts': data['message_ts'],
#             'as_user': True
#             }
#
# def send_message(channel_id, message):
#     client.api_call(
#         "chat.postMessage",
#         channel=channel_id,
#         text=message,
#         username='test-bot',
#         icon_emoji=':robot_face:'
#     )

