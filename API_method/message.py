# -*- coding: utf-8 -*-
import json
import re


'''
All methods for manipulating the private messages: 
Open file that has template
Give attributes to each PM
Replace template with actual values using regex/ dictionary
'''

class PrivateMessage:
    
    message_location = 'messages.json'  # default location
    
    def __init__(self, message_type, replace_dict):        
        self.channel = ""
        self.timestamp = ""
        self.text = self.open_json_messages(message_type)
        self.text = self.replace_string(self.text, replace_dict)
    
    # opens json file; is converted to a dict{str:[list]} 
    # input- message_type:str is the dictionary keys
    # returns dictionary list    
    def open_json_messages(self, message_type):
        with open(self.message_location) as json_file:
            json_dict = json.load(json_file)
            
            # returns a string, with newline char between eachlist item. 
            return '\n'.join(json_dict[message_type])  
    
    def replace_string_chars(self, message_string, replace_dictionary):
        
        # replace_dictionary = {'String_to_replace': 'new_string', 'String_to_replace_2': 'new_string2'}
        # we want to find keys in the replace_dictionary that are between {{  }} 
        # find all {{ }}
        ###########(group1)(group2)(group3)(group4)(group5) group3 = dict key
        regex_string = r'(\{\{)( {0,4})(\w*)( {0,4})(\}\})'
        template = re.compile(regex_string)
        regex_match = template.match(message_string)
        while(regex_match):
        
            # get the dictionary value by the group3 match
            # get call rather than using brackets prevents Exception
            insert_text = replace_dictionary.get(regex_match.group(3))
            if insert_text:
                message_string = message_string[:regex_match.start()] + insert_text  + message_string[regex_match.end():]
            
            regex_match = template.match(message_string)
        return message_string   
    
    
if __name__ == '__main__':
    test1 = PrivateMessage('new_greeting')
    
    testdict = {'UserName': 'Will', 'TestName': None}    
    found_string = '{{ UserName }}  {{ TestName }} is this going to work?'
    
    fixed_string = test1.replace_string_chars(found_string, testdict)
    print(found_string)
    print(fixed_string)
    