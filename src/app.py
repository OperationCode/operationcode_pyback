import logging
import time
from slackclient import SlackClient
from utils.log_manager import setup_logging
from decouple import config
import traceback

from src.help_menu import HELP_MENU_RESPONSES
from src.messages import HELP_MENU, MESSAGE, needs_greet_button, greeted_response_attachments

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')
all_event_logger = logging.getLogger(f'{__name__}.all_events')

# constants
PROXY = config('PROXY')

# TOKEN = config('PERSONAL_APP_TOKEN')
# COMMUNITY_CHANNEL = config('PERSONAL_PRIVATE_CHANNEL')

TOKEN = config('OPCODE_APP_TOKEN')
COMMUNITY_CHANNEL = config('OPCODE_REWRITE_CHANNEL')
PROJECTS_CHANNEL = config('OPCODE_OC_PROJECTS_CHANNEL')
# COMMUNITY_CHANNEL = config('OPCODE_COMMUNITY_ID')

PROXY = PROXY if PROXY else None
slack_client = SlackClient(TOKEN, proxies=PROXY)


# TODO: Do something with all of the return values here

def build_message(message_template: str, **kwargs: dict) -> str:
    return message_template.format(**kwargs)


def event_handler(event_dict: dict) -> None:
    """
    Handles routing all of the received subscribed events to the correct method
    :param event_dict:
    """
    # all_event_logger.info(event_dict)
    if event_dict['type'] == 'team_join':
        new_event_logger.info('New member event recieved')
        new_member(event_dict)

    """ Trigger for testing team_join event """
    if event_dict['type'] == 'message' and 'user' in event_dict.keys() and event_dict['text'] == 'testgreet':
        event_dict['user'] = {'id': event_dict['user']}
        new_member(event_dict)


def help_menu_interaction(data: dict) -> None:
    """
    Receives help menu selection from the user and dynamically updates
    displayed message
    :param data:
    """
    params = {'text': '  \n\n\n' + HELP_MENU_RESPONSES[data['actions'][0]['value']],
              'channel': data['channel']['id'],
              'ts': data['message_ts'],
              'as_user': True
              }
    slack_client.api_call('chat.update', **params)


def greeted_interaction(data: dict) -> dict:
    """
    Handles the interactive message sent to the #community channel
    when a new member joins.

    Displays the user that claimed the greeting along with the option
    to un-claim
    """
    if data['actions'][0]['value'] == 'greeted':
        clicker = data['user']['id']
        params = {'text': data['original_message']['text'],
                  "attachments": greeted_response_attachments(clicker),
                  'channel': data['channel']['id'],
                  'ts': data['message_ts'],
                  'as_user': True
                  }
        res = slack_client.api_call("chat.update", **params)
        return res
    elif data['actions'][0]['value'] == 'reset_greet':
        params = {'text': data['original_message']['text'],
                  "attachments": needs_greet_button(),
                  'channel': data['channel']['id'],
                  'ts': data['message_ts'],
                  'as_user': True
                  }
        res = slack_client.api_call("chat.update", **params)


def new_member(event_dict: dict) -> None:
    new_event_logger.info('Recieved json event: {}'.format(event_dict))

    user_id = event_dict['user']['id']
    logging.info('team_join message')

    real_name = user_name_from_id(user_id)

    custom_message = MESSAGE.format(real_name=real_name)

    new_event_logger.info('Built message: {}'.format(custom_message))
    response = slack_client.api_call('chat.postMessage',
                                     channel=user_id,
                                     # channel=COMMUNITY_CHANNEL, #  testing option
                                     # as_user=True,  # Currently not working.  DM comes from my account
                                     text=custom_message)

    r2 = slack_client.api_call('chat.postMessage',
                               channel=user_id,
                               # channel=COMMUNITY_CHANNEL, #  testing option
                               # as_user=True,
                               **HELP_MENU)

    # Notify #community
    text = f":tada: <@{user_id}> has joined the Slack team :tada:"
    slack_client.api_call('chat.postMessage', channel=COMMUNITY_CHANNEL,
                          text=text, attachments=needs_greet_button())

    if response['ok']:
        new_event_logger.info('New Member Slack response: Response 1: {} \nResponse2: {}'.format(response, r2))
    else:
        new_event_logger.error('FAILED -- Message to new member returned error: {}'.format(response))


def parse_slack_output(slack_rtm_output: list) -> None:
    """
    Method for parsing slack events when using the RTM API instead
    of the Events/App APIs
    """
    for output in slack_rtm_output:
        # process a single item in list at a time
        event_handler(output)


def user_name_from_id(user_id: str) -> str:
    """
    Queries the Slack workspace for the users real name
    to personalize messages.  Prioritizes real_name -> name -> 'New Member'
    :param user_id:
    """
    response = slack_client.api_call('users.info', user=user_id)

    if response['user']['real_name']:
        return response['user']['real_name'].title()
    elif response['user']['name']:
        return response['user']['name'].title()
    else:
        return 'New Member'


def join_channels():
    """
    Utility function for joining channels.  Move to utils?
    """
    response = slack_client.api_call('channels.join', name='general')
    print(response)


# set the defalt to a 1 second delay
def run_bot(delay: int=1) -> None:
    """
    Runs the bot using the Slack Real Time Messaging API.
    **Doesn't provide events or interactive functionality
    :param delay:
    """
    setup_logging()
    if slack_client.rtm_connect():
        print(f"StarterBot connected and running with a {delay} second delay")

        while True:
            try:
                parse_slack_output(slack_client.rtm_read())
                time.sleep(delay)
            except Exception as e:
                logger.error(f'Some exception occured: {e}')
                logger.error(f'traceback: {traceback.print_exc()}')
                slack_client.rtm_connect()
    else:
        print("Connection failed.  Invalid Slack token or bot ID")


if __name__ == '__main__':
    run_bot()
