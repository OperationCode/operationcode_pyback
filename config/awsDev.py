from decouple import config

PORT = 5000

TOKEN = config('DEV_BOT_TOKEN', default='token')
VERIFICATION_TOKEN = config('DEV_AUTH_TOKEN', default='token')
COMMUNITY_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'

DB_USERNAME = config('AWS_DEV_DB_USERNAME', default='')
DB_PASSWORD = config('AWS_DEV_DB_PASSWORD', default='')
DB_DIALECT = config('AWS_DEV_DB_DIALECT', default='sqlite')
DB_ADDR = config('AWS_DEV_DB_ADDR', default='dev.db')
DB_NAME = config('AWS_DEV_DB_NAME', default='')
