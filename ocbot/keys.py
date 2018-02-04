from decouple import config

# app verification tokens
VERIFICATION_TOKEN = config('OPCODE_VERIFICATION_TOKEN')
# VERIFICATION_TOKEN = config('APP_VERIFICATION_TOKEN', default='token')
# VERIFICATION_TOKEN = config('TEST2_AUTH_TOKEN', default='token')

# from src.airtable_handling import airtable

# Workspace token selection
TOKEN = config('OPCODE_TOKEN')
# TOKEN = config('PERSONAL_APP_TOKEN', default='token')
# TOKEN = config('TEST2_BOT_TOKEN', default='token')
# TOKEN = config('OPCODE_APP_TOKEN')


# community channel selections
# COMMUNITY_CHANNEL = config('OPCODE_COMMUNITY_ID')
COMMUNITY_CHANNEL = config('OPCODE_BOT_TESTING_CHANNEL')
# COMMUNITY_CHANNEL = config('PERSONAL_PRIVATE_CHANNEL', default='community_channel')
# COMMUNITY_CHANNEL = config('TEST2_PRIVATE_CHANNEL', default='community_channel')
# COMMUNITY_CHANNEL = config('OPCODE_REWRITE_CHANNEL')
# PROJECTS_CHANNEL = config('OPCODE_OC_PROJECTS_CHANNEL')

# airtable config selections
AIRTABLE_BASE_KEY = config('PERSONAL_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('PERSONAL_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'
#AIRTABLE_BASE_KEY = config('OPCODE__AIRTABLE_BASE_KEY')
#AIRTABLE_API_KEY = config('OPCODE_AIRTABLE_TOKEN')
#AIRTABLE_TABLE_NAME = 'Mentor Request'


# database stuff
# postgres config selections
# PG_USERNAME = config('PERSONAL_PG_USERNAME')
# PG_PASSWORD = config('PERSONAL_PG_PASSWORD')
# PG_URL = config('PERSONAL_PG_URL')
PG_USERNAME = config('PG_USERNAME', default=None)
PG_PASSWORD = config('PG_PASSWORD', default=None)
PG_URL = config('PG_URL', default=None)


# PythonAnywhere SSH Tunnel Configurations
PA_SSH_USERNAME = config('PA_SSH_USERNAME', default=None)
PA_SSH_PASSWORD = config('PA_SSH_PASSWORD', default=None)
PA_SSH_URL = config('PA_SSH_URL', default=None)
PA_SSH_REMOTE_BIND_ADDR = config('PA_PG_IP_ADDR', cast=str, default=None)
PA_SSH_REMOTE_BIND_PORT = config('PA_PG_PORT', cast=int, default=0)
