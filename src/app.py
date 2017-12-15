import logging
import time

import requests
from slackclient import SlackClient

from keys import TOKEN, COMMUNITY_CHANNEL, AIRTABLE_API_KEY, AIRTABLE_BASE_KEY, AIRTABLE_TABLE_NAME
from src.help_menu import HELP_MENU_RESPONSES
from src.messages import *
from utils.log_manager import setup_logging

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')

slack_client = SlackClient(TOKEN)


# TODO: Do something with all of the return values here

def build_message(message_template: str, **kwargs: dict) -> str:
    return message_template.format(**kwargs)


def event_handler(event_dict: dict) -> None:
    """
    Handles routing all of the received subscribed events to the correct method
    :param event_dict:
    """

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

    response = data['actions'][0]['value']

    if response == 'suggestion':
        trigger_id = data['trigger_id']
        response = slack_client.api_call('dialog.open', trigger_id=trigger_id, dialog=SUGGESTION_MODAL)

    # Disabled while airtable integration is still in development
    # elif response == 'mentor':
    #     trigger_id = data['trigger_id']
    #     res = slack_client.api_call('dialog.open', trigger_id=trigger_id, dialog=MENTOR_REQUEST_MODAL)
    #     pprint(res)

    else:
        params = {'text': HELP_MENU_RESPONSES[data['actions'][0]['value']],
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


def suggestion_submission(data: dict) -> None:
    """
    Receives the event when a user submits a suggestion for a new help topic and
    posts it to the #community channel
    :param data:
    """
    suggestion = data['submission']['suggestion']
    user_id = data['user']['id']
    message = f":exclamation:<@{user_id}> just submitted a suggestion for a help topic:exclamation:\n-- {suggestion}"
    res = slack_client.api_call('chat.postMessage', channel=COMMUNITY_CHANNEL, text=message)


def mentor_submission(data):
    """
    Parses the mentor request dialog form and pushes the data to Airtable.
    :param data:
    :return:
    """

    # Temporary hack.  Change this to getting the record ID's from the table itself
    services_records = {
        'General Guidance - Slack Chat': 'recBxmDasLXwmVB78',
        'General Guidance - Voice Chat': 'recDyu4PMbPl7Ti58',
        'Pair Programming': 'recHCFAO9uNSy1WDs',
        'Code Review': 'recUK55xJXOfAaYNb',
        'Resume Review': 'recXZzUduWfaxWvSF',
        'Mock Interview': 'recdY4XLeN1CPz1l8'
    }

    form = data['submission']
    params = {
        'fields': {
            'Slack User': form['Slack User'],
            'Email': form['Email'],
            'Service': [services_records[form['service']]],
            'Skillsets': [form['skillset']],
            'Additional Details': form['Additional Details']
        }
    }

    headers = {
        'authorization': "Bearer " + AIRTABLE_API_KEY
    }
    res = requests.post(f"https://api.airtable.com/v0/{AIRTABLE_BASE_KEY}/{AIRTABLE_TABLE_NAME}", json=params,
                        headers=headers)


def new_member(event_dict: dict) -> None:
    """
    Invoked when a new user joins and a team_join event is received.
    DMs the new user with the welcome message and help menu as well as pings
    the #community channel with a new member notification
    :param event_dict:
    """
    new_event_logger.info('Recieved json event: {}'.format(event_dict))

    user_id = event_dict['user']['id']
    logging.info('team_join message')

    real_name = user_name_from_id(user_id)

    custom_message = MESSAGE.format(real_name=real_name)

    new_event_logger.info('Built message: {}'.format(custom_message))
    response = slack_client.api_call('chat.postMessage',
                                     channel=user_id,
                                     # channel=COMMUNITY_CHANNEL, #  testing option
                                     as_user=True,  # Currently not working.  DM comes from my account
                                     text=custom_message)

    r2 = slack_client.api_call('chat.postMessage',
                               channel=user_id,
                               # channel=COMMUNITY_CHANNEL,  # testing option
                               as_user=True,
                               **HELP_MENU)

    # Notify #community
    text = f":tada: <@{user_id}> has joined the Slack team :tada:"
    slack_client.api_call('chat.postMessage', channel=COMMUNITY_CHANNEL,
                          text=text, attachments=needs_greet_button())

    if response['ok'] and r2['ok']:
        new_event_logger.info('New Member Slack response: Response 1: {} \nResponse2: {}'.format(response, r2))
    else:
        new_event_logger.error('FAILED -- Message to new member returned error: {}\n{}'.format(response, r2))


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


def run_bot(delay: int = 1) -> None:
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
                logger.exception(e)
                slack_client.rtm_connect()
    else:
        print("Connection failed.  Invalid Slack token or bot ID")


if __name__ == '__main__':
    run_bot()
