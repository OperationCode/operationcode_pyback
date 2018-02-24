from decouple import config

PORT = 5000

TOKEN = config('TEST2_BOT_TOKEN', default='token')
VERIFICATION_TOKEN = config('TEST2_AUTH_TOKEN', default='token')
COMMUNITY_CHANNEL = config('TEST2_PRIVATE_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('TEST2_PRIVATE_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('PERSONAL_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('PERSONAL_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'

PG_USERNAME = config('PERSONAL_PG_USERNAME', default='username')
PG_PASSWORD = config('PERSONAL_PG_PASSWORD', default='password')
PG_URL = config('PERSONAL_PG_URL', default='url')

PA_SSH_USERNAME = config('PA_SSH_USERNAME', default=None)
PA_SSH_PASSWORD = config('PA_SSH_PASSWORD', default=None)
PA_SSH_URL = config('PA_SSH_URL', default=None)
PA_SSH_REMOTE_BIND_ADDR = config('PA_PG_IP_ADDR', cast=str, default=None)
PA_SSH_REMOTE_BIND_PORT = config('PA_PG_PORT', cast=int, default=0)
