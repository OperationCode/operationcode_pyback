from .utils import ResponseContainer
from slackclient import SlackClient
from .utils import verify_module_variable
import logging
from functools import partial

logger = logging.getLogger(__name__)

_slack_config = {}


def SlackStart(api_key=None, verification_token=None):
    _slack_config['API_KEY'] = api_key
    _slack_config['VERIFICATION_TOKEN'] = verification_token
    _slack_config['client'] = SlackClient(_slack_config['API_KEY'])


@verify_module_variable(['VERIFICATION_TOKEN', 'API_KEY'], _slack_config, 'slack')
class SlackBuilder:
    """
    user_id and flattened dict get passed
    """

    # TODO determine if need as_user
    @staticmethod
    def message(self, channel, **message_payload):
        return ResponseContainer(route='Slack',
                                 method='chat.postMessage',
                                 payload=dict(channel=channel,
                                               as_user=True,  # optional?
                                               **message_payload))

    @staticmethod
    def update(self, channel, **message_payload):
        return ResponseContainer(route='Slack',
                                 method='chat.update',
                                 payload=dict(channel=channel,
                                               **message_payload))


@verify_module_variable(['VERIFICATION_TOKEN', 'API_KEY'], _slack_config, 'slack')
class Slack:

    # TODO add exception handling for the cases
    def user_name_from_id(self, user_id: str) -> str:
        """
        Queries the Slack workspace for t   he users real name
        to personalize messages.  Prioritizes real_name -> name -> 'New Member'
        :param user_id:
        """
        print('hi there')
        response = _slack_config['client'].api_call('users.info', user=user_id)

        if response['user']['real_name']:
            return response['user']['real_name'].title()
        elif response['user']['name']:
            return response['user']['name'].title()
        else:
            return 'New Member'

            # TODO add exception handling for the cases

    def __getattr__(self, name):
        """
        called when getattr(self, name) is not found
        :return:
        :rtype:
        """
        default = partial(self.default, name)
        return default

    def default(self, method, payload):
        print(f'default found.... {method}, {payload}')
        response = _slack_config['client'].api_call(method, **payload)

    def is_slack_success(response_list: List[ResponseContainer], event_key: UUID) -> bool:

        for item in response_list:
            try:
                client.api_call(item.call_method, **item.response)
                yield True
            except Exception as response:
                logging.exception(response, UUID)
                yield False


def build_message(message_template: str, **kwargs: dict) -> str:
    return message_template.format(**kwargs)


def get_response_type(response_data):
    return response_data['actions'][0]['value']


def join_channels():
    """
    Utility function for joining channels.  Move to utils?
    """
    client.api_call('channels.join', name='general')


def make_base_params(data, text_value, ):
    return {'text': text_value,
            'channel': data['channel']['id'],
            'ts': data['message_ts'],
            'as_user': True
            }


def user_name_from_id(user_id: str) -> str:
    """
    Queries the Slack workspace for t   he users real name
    to personalize messages.  Prioritizes real_name -> name -> 'New Member'
    :param user_id:
    """
    response = client.api_call('users.info', user=user_id)

    if response['user']['real_name']:
        return response['user']['real_name'].title()
    elif response['user']['name']:
        return response['user']['name'].title()
    else:
        return 'New Member'


def list_channels():
    channels_call = client.api_call("channels.list")
    return channels_call['channels'] if channels_call.get('ok') else None


def print_channels():
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            print(channel['name'] + " (" + channel['id'] + ")")
            # detailed_info = channel_info(channel['id'])
            # if detailed_info:
            #     if detailed_info['members']:
            #         print([x for x in detailed_info['members']])
            # print('Latest text from ' + channel['name'] + ":")
            # print(detailed_info['latest']['text'])
        print('-----')
    else:
        print("Unable to authenticate.")


def send_message(channel_id, message):
    client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='test-bot',
        icon_emoji=':robot_face:'
    )


def get_bot_id(bot_name):
    api_call = client.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') is bot_name:
                print(f"Bot ID for {user['name']} is {user.get('id')}")
    else:
        print(f"Could not find bot user with the name {bot_name}")