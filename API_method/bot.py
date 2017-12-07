'''
Main bot routing


'''

from slackclient import SlackClient

from API_method.CredManager import CredManager
from API_method.message import PrivateMessage

authed_teams = {'T03GSNF5H' : None}  # location to store the Oauth token during a session.

# 	user_id: 'U4K0GHV54',
#   team_id: 'T03GSNF5H'

class Bot(object):
    ''' Instances a Bot object to handle Slack onboarding interactions.'''
    def __init__(self, cred_call_name=None):
        super(Bot, self).__init__()
        self.name = 'OP Code Greet Bot'
        self.emoji = ':robot_face:'
        
        # access cred manager
        self.oauth = CredManager().get_creds_dict(cred_file_name=cred_call_name)      
        
        self.oauth['scope'] = 'bot'   # most limited permissions-
        
        
        self.verification = self.oauth['verification_token'] # link token to this bot
        
        # need empty SlackClient call to generate OAuth token
        self.client = SlackClient("")
        
        # temp storage of each message
        self.messages = {}

        
    '''
    auth the bot and with correct permissions: bot
    input- temp_auth_code: str  (temporary 
    ''' 
    def auth(self, temp_auth_code):

        auth_response = self.client.api_call(
                                "oauth.access",
                                client_id=self.oauth["client_id"],
                                client_secret=self.oauth["client_secret"],
                                code=temp_auth_code
                                )

        # store auth response in file dictionary
        team_id = auth_response["team_id"]
        authed_teams[team_id] = {"bot_token":
                                 auth_response["bot"]["bot_access_token"]}
        
        # update client witht his team id token
        self.client = SlackClient(authed_teams[team_id]["bot_token"])
    
    '''
    Open a DM
    input- user_id: str
    output (dm channel) - dm_id: str
    '''
    def open_dm(self, user_id):
        new_dm = self.client.api_call("im.open",
                                      user=user_id)
        dm_id = new_dm["channel"]["id"]
        return dm_id
       
    
    '''
    Create and send  message to new user, store message in the class item 'self.message'
    input- user_id: str; team_id: str
    '''    
    def onboarding_message(self, team_id, user_id):
        
        # get new message
        replace_dict = {'UserName': 'testid'}
        message_obj = PrivateMessage('team_join', replace_dict)
        
        self.messages[user_id] = message_obj
        message_obj.channel = self.open_dm(user_id)
        
        post_message = self.client.api_call("chat.postMessage",
                                            channel=message_obj.channel,
                                            username=self.name,
                                            icon_emoji=self.emoji,
                                            text=message_obj.text                                            
                                            )
        timestamp = post_message["ts"]

        message_obj.timestamp = timestamp