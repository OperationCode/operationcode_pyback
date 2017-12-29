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


#@verify_module_variable(['VERIFICATION_TOKEN', 'API_KEY'], _slack_config, 'slack')
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

