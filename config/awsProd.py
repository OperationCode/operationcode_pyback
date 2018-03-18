from decouple import config

DEBUG = False

TOKEN = config('PROD_BOT_TOKEN')
VERIFICATION_TOKEN = config('PROD_AUTH_TOKEN')
COMMUNITY_CHANNEL = config('PROD_COMMUNITY_CHANNEL')
MENTORS_INTERNAL_CHANNEL = config('PROD_MENTOR_CHANNEL')

AIRTABLE_BASE_KEY = config('PROD_AIRTABLE_BASE_KEY')
AIRTABLE_API_KEY = config('PROD_AIRTABLE_TOKEN')
AIRTABLE_TABLE_NAME = 'Mentor Request'

DB_USERNAME = config('PROD_DB_USERNAME', default='')
DB_PASSWORD = config('PROD_DB_PASSWORD', default='')
DB_DIALECT = config('PROD_DB_DIALECT', default='sqlite')
DB_ADDR = config('PROD_DB_ADDR', default='dev.db')
DB_NAME = config('PROD_DB_NAME', default='')
