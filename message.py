# -*- coding: utf-8 -*-
"""
Python Slack Message class for use with the pythOnBoarding bot
"""

import json


message_location = 'all_messages.json'

class Message:
            
    def __init__(self, message_type):
        super(Message, self).__init__()
        self.channel = ""
        self.timestamp = ""
        self.text = open_json_messages(message_type)
       

    # get type, and string.                         
    def open_json_messages(self, message_type):
        with open(message_location) as json_file:
            json_dict = json.load(json_file)
            json_attachments = json_dict[message_type]
    
    
    