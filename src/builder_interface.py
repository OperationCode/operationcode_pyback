from typing import NamedTuple, List

from src.messagesnew import text_greet, external_buttons, resources, default_interest
from utils.slack_utils import *
from keys import COMMUNITY_CHANNEL
from src.messages import needs_greet_button

SlackContainer = NamedTuple('SlackContainer', [('call_type', str), ('response', dict)])
'''
container for a single slack api call
'''


# TODO Adjust default values so they aren't only ruby, python, JS.
def get_default_vals() -> List[dict]:
    """
    Get's the original default values for the button in the greet
    :param None
    :return:default_interest
    :rtype: List[dict]
    """
    return default_interest


def interest_builder_call(event_dict: dict) -> List[dict]:
    """
    :param event_dict:
    :type event_dict:
    :return: interest_list
    :rtype: List[dict]
    """
    # call the db for interests of a user
    # get values from resources.yaml
    # if error we go with default.
    interest_list = get_default_vals()
    return interest_list


def new_member(event_dict: dict) -> List[SlackContainer]:
    """
    Invoked when a new user joins and a team_join event is received.
    DMs the new user with the welcome message and help menu as well as pings
    the #community channel with a new member notification
    :param event_dict: dict
    :param interests: dict
    """
    # external calls
    # slack id call
    user_id = event_dict['user']['id']
    message_text = text_greet.format(real_name=user_name_from_id(user_id))
    # database user call
    interests = interest_builder_call(event_dict)

    # use the external calls
    community_text = f":tada: <@{user_id}> has joined! :tada:"
    building_resources = resources
    building_resources['attachments']['actions'] = interests

    # build responses
    built_list = []
    built_list.append(SlackContainer(call_type='chat.postMessage',
                                     response=dict(channel=user_id,
                                                   as_user=True,
                                                   text=message_text)
                                     )
                      )
    built_list.append(SlackContainer(call_type='chat.postMessage',
                                     response=dict(channel=user_id,
                                                   as_user=True,
                                                   **external_buttons
                                                   )
                                     )
                      )
    built_list.append(SlackContainer(call_type='chat.postMessage',
                                     response=dict(channel=user_id,
                                                   as_user=True,
                                                   **building_resources
                                                   )
                                     )
                      )
    built_list.append(SlackContainer(call_type='chat.postMessage',
                                     response=dict(channel=COMMUNITY_CHANNEL,
                                                   text=community_text,
                                                   attachments=needs_greet_button())
                                     )
                      )

    return built_list
