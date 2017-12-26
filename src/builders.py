import logging

from requests import Response, post
from slackclient import SlackClient

from keys import *
from src.help_menu import HELP_MENU_RESPONSES
from src.messages import *
from utils import get_response_type, make_base_params, user_name_from_id

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')

slack_client = SlackClient(TOKEN)


def help_menu_interaction(data: dict) -> dict:
    """
    Receives help menu selection from the user and dynamically updates
    displayed message
    :param data: dict
    :returns response: dict
    """
    response = None
    response_type = get_response_type(data)

    if response_type is 'suggestion':
        trigger_id = data['trigger_id']
        response = slack_client.api_call('dialog.open',
                                         trigger_id=trigger_id,
                                         dialog=SUGGESTION_MODAL)

    elif response_type is 'mentor':
        pass
        # trigger_id = data['trigger_id']
        # Disabled while airtable integration is still in development
        # slack_client.api_call('dialog.open',
        #                            trigger_id=trigger_id,
        #                            dialog=MENTOR_REQUEST_MODAL)

    else:
        params = make_base_params(data, HELP_MENU_RESPONSES[response_type])
        response = slack_client.api_call('chat.update', **params)
    return response


def greeted_interaction(data: dict) -> dict:
    """
    Handles the interactive message sent to the #community channel
    when a new member joins.

    Displays the user that claimed the greeting along with the option
    to un-claim
    """
    greet_type = get_response_type(data)

    params = make_base_params(data, data['original_message']['text'])

    if greet_type is 'greeted':
        clicker = data['user']['id']
        params['attachments'] = greeted_response_attachments(clicker)

    # greet_type is 'reset_greet'
    else:
        params['attachments'] = needs_greet_button()

    return slack_client.api_call("chat.update", **params)


def suggestion_submission(data: dict) -> dict:
    """
    Receives the event when a user submits a suggestion for a new help topic and
    posts it to the #community channel
    :param data:
    """
    suggestion = data['submission']['suggestion']
    user_id = data['user']['id']
    message = (f":exclamation:<@{user_id}>"
               " just submitted a suggestion for a help topic:exclamation:\n-- "
               f"{suggestion}")

    return slack_client.api_call('chat.postMessage',
                                 channel=COMMUNITY_CHANNEL,
                                 text=message)


def mentor_submission(event_dict: dict) -> Response:
    """
    Parses the mentor request dialog form and pushes the data to Airtable.
    :param event_dict : dict
    :return response: Response
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

    form = event_dict['submission']
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
    return post(f"https://api.airtable.com/v0/{AIRTABLE_BASE_KEY}/{AIRTABLE_TABLE_NAME}",
                json=params,
                headers=headers)


def new_member(event_dict: dict) -> None:
    """
    Invoked when a new user joins and a team_join event is received.
    DMs the new user with the welcome message and help menu as well as pings
    the #community channel with a new member notification
    :param event_dict: dict

    """
    logging.info('team_join message')
    logging.info('Recieved json event: {}'.format(event_dict))

    user_id = event_dict['user']['id']
    custom_message = MESSAGE.format(real_name=user_name_from_id(user_id))
    new_event_logger.info(f'Built message: {custom_message}')

    text_response = slack_client.api_call('chat.postMessage',
                                          channel=user_id,
                                          # channel=COMMUNITY_CHANNEL, #  testing option
                                          as_user=True,  # Currently not working.  DM comes from my account
                                          text=custom_message)

    button_response = slack_client.api_call('chat.postMessage',
                                            channel=user_id,
                                            # channel=COMMUNITY_CHANNEL,  # testing option
                                            as_user=True,
                                            **HELP_MENU)

    # Notify #community
    community_text = f":tada: <@{user_id}> has joined! :tada:"
    community_response = slack_client.api_call('chat.postMessage',
                                               channel=COMMUNITY_CHANNEL,
                                               text=community_text,
                                               attachments=needs_greet_button())

    if text_response['ok'] and button_response['ok'] and community_response['ok']:
        new_event_logger.info(f'New Member Slack response-> '
                              f'text: {text_response} \n'
                              f'button: {button_response} \n'
                              f'community response: {community_response}')
    else:
        new_event_logger.error('FAILED -- Message to new member returned '
                               f'error: {text_response} \n'
                               f'button: {button_response}\n'
                               f'community response: {community_response}')
