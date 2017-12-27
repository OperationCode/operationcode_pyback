from slackclient import SlackClient

from keys import TOKEN

client = SlackClient(TOKEN)


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


if __name__ == '__main__':
    from decouple import config

    TOKEN = config('OPCODE_APP_TOKEN')
    client = SlackClient(TOKEN)
    print_channels()
