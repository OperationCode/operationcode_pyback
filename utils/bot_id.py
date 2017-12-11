import os

from slackclient import SlackClient
from archived.creds import TOKEN

BOT_NAME = 'testopcode'

slack_client = SlackClient(TOKEN)

if __name__ == '__main__':
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print(f"Bot ID for {user['name']} is {user.get('id')}")
    else:
        print(f"Could not find bot user with the name {BOT_NAME}")