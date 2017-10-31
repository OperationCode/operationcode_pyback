import json


'''  
    1. Get's saved credentials and converts to dictionary
    2. Pass in Credential in a dictionary and save it to another file (Later refresh token)
    
    Desired:
    1. Exception I/O handling (missing file, file in use, incorrect file name).
'''
class CredentialManager:
    default_creds = 'credentials.json' # default cred file name
        
    def get_creds_dict(self, cred_file_name=None): # if other credential file name we load that file
        if cred_file_name is None:
            cred_file_name = self.default_creds  
        
        with open(cred_file_name, 'r') as creds:
            return json.load(creds)
           

    def write_creds_dict(self, cred_dict, cred_file_name=None):
        if cred_file_name is None:
           cred_file_name = self.default_creds
        
        with open(cred_file_name, 'w') as f:
            json.dump(cred_dict, f, ensure_ascii=False)
  
if __name__ == '__main__':

    '''credentials = {'access_secret': '392n39d93',
           'access_token': 'sdf424f',
           'consumer_key': 'sdf3223',
           'consumer_secret': 'dsf2344'}  '''
           
    # CredentialManager().write_creds_dict(credentials)
    # CredentialManager().get_creds_dict()
