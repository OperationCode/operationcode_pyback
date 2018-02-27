from decouple import config

PORT = 5000

TOKEN = config('PERSONAL_BOT_TOKEN', default='token')
VERIFICATION_TOKEN = config('APP_VERIFICATION_TOKEN', default='token')
COMMUNITY_CHANNEL = config('PERSONAL_PRIVATE_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('PERSONAL_PRIVATE_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'

DB_USERNAME = config('DEV_DB_USERNAME', default='')
DB_PASSWORD = config('DEV_DB_PASSWORD', default='')
DB_DIALECT = config('DEV_DB_DIALECT', default='sqlite')
DB_ADDR = config('DEV_DB_ADDR', default='dev.db')
DB_NAME = config('DEV_DB_NAME', default='')

PA_SSH_USERNAME = config('PA_SSH_USERNAME', default=None)
PA_SSH_PASSWORD = config('PA_SSH_PASSWORD', default=None)
PA_SSH_URL = config('PA_SSH_URL', default=None)
PA_SSH_REMOTE_BIND_ADDR = config('PA_PG_IP_ADDR', cast=str, default=None)
PA_SSH_REMOTE_BIND_PORT = config('PA_PG_PORT', cast=int, default=0)
