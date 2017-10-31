# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the pythOnBoarding app
"""
import os
import message

from slackclient import SlackClient
import CredentialManager

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
authed_teams = {'T03GSNF5H' : None}

# 	user_id: 'U4K0GHV54',
#   team_id: 'T03GSNF5H'

class Bot(object):
    """ Instanciates a Bot object to handle Slack onboarding interactions."""
    def __init__(self, cred_call_name=None):
        super(Bot, self).__init__()
        self.name = 'OP Code Greet Bot'
        self.emoji = ':robot_face:'
        
        # access cred manager
        self.oauth = CredentialManager().get_creds_dict(cred_file_name=cred_call_name)        
        self.oauth['scope'] = 'bot'   # most limited permissions-
        
        # link token to this bot, for app to handle requests
        self.verification = self.oauth['verification_token']
        
        
        
        # need empty SlackClient call to generate OAuth token
        self.client = SlackClient("")
        
        # temp storage of each message
        self.messages = {}

    def auth(self, code):
        """
        Authenticate with OAuth and assign correct scopes.
        Save a dictionary of authed team information in memory on the bot
        object.

        Parameters
        ----------
        code : str
            temporary authorization code sent by Slack to be exchanged for an
            OAuth token

        """
        # After the user has authorized this app for use in their Slack team,
        # Slack returns a temporary authorization code that we'll exchange for
        # an OAuth token using the oauth.access endpoint
        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=code
                                )
        # To keep track of authorized teams and their associated OAuth tokens,
        # we will save the team ID and bot tokens to the global
        # authed_teams object
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        # Then we'll reconnect to the Slack Client with the correct team's
        # bot token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])

    def open_dm(self, user_id):
        """
        Open a DM to send a welcome message when a 'team_join' event is
        recieved from Slack.

        Parameters
        ----------
        user_id : str
            id of the Slack user associated with the 'team_join' event

        Returns
        ----------
        dm_id : str
            id of the DM channel opened by this method
        """
        new_dm = self.client.api_call("im.open",
                                      user=user_id)
        dm_id = new_dm["channel"]["id"]
        return dm_id

    def onboarding_message(self, team_id, user_id):
        """
        Create and send an onboarding welcome message to new users. Save the
        time stamp of this message on the message object for updating in the
        future.

        Parameters
        ----------
        team_id : str
            id of the Slack team associated with the incoming event
        user_id : str
            id of the Slack user associated with the incoming event

        """

        self.messages[team_id] = {user_id: message.Message()}
        message_obj = self.messages[team_id][user_id]
        # Then we'll set that message object's channel attribute to the DM
        # of the user we'll communicate with
        message_obj.channel = self.open_dm(user_id)

        post_message = self.client.api_call("chat.postMessage",
                                            channel=message_obj.channel,
                                            username=self.name,
                                            icon_emoji=self.emoji,
                                            text=message_obj.text,
                                            text=message_obj.text,
                                            )
        timestamp = post_message["ts"]

        message_obj.timestamp = timestamp
  
    
