from .utils import ResponseContainer
from .utils import verify_module_variable
from requests import post
from functools import partial

_airtableconfig = {}


def AirTableStart(api_key=None, table_key=None, table_name=None):
    _airtableconfig['API_KEY'] = api_key
    _airtableconfig['TABLE_NAME'] = table_name
    _airtableconfig['TABLE_KEY'] = table_key


# @verify_module_variable(['API_KEY', 'TABLE_NAME', 'TABLE_KEY'], _airtableconfig, 'airtable')
class AirTableBuilder:
    # Temporary hack.  Change this to getting the record ID's from the table itself
    _services_records = {
        'General Guidance - Slack Chat': 'rec7TQyPoFMHGEARz',
        'General Guidance - Voice Chat': 'rec9UYZuI5EwrChPz',
        'Pair Programming': 'recdY9vt5oC3SKVnT',
        'Code Review': 'recq6z0cFRDqUTXxC',
        'Resume Review': 'rectl3PSqQ4lRFuC6',
        'Mock Interview': 'recJkySqaHQN9i05z'
    }

    @classmethod
    def record_to_service(cls, record: str) -> str:

        #  Test Airtable services.  These will all be moved somewhere else
        #  eventually (maybe)
        # services = {
        #     'rec7TQyPoFMHGEARz': 'General Guidance - Slack Chat',
        #     'rec9UYZuI5EwrChPz': 'General Guidance - Voice Chat',
        #     'recdY9vt5oC3SKVnT': 'Pair Programming',
        #     'recq6z0cFRDqUTXxC': 'Code Review',
        #     'rectl3PSqQ4lRFuC6': 'Resume Review',
        #     'recJkySqaHQN9i05z': 'Mock Interview'
        # }
        services = {
            'recry8s14qGJhHeOC': 'General Guidance - Slack Chat',
            'rectzgTGoQyy2FVMC': 'General Guidance - Voice Chat',
            'recxDrpFL9w5tNzkW': 'Pair Programming',
            'recKLRUolCxsvWBuF': 'Code Review',
            'recN0lJ46BYnsI8z9': 'Resume Review',
            'rec3ZQMCQsKPKlE2C': 'Mock Interview'
        }
        return services[record]

    @classmethod
    def entry(cls, params):
        return ResponseContainer(route='AirTable',
                                 method='raw',
                                 payload=dict(url=cls.build_url,
                                              json=params,
                                              headers=cls.build_header()
                                              )
                                 )

    @classmethod
    def record(cls, record_key):
        return cls._services_records[record_key]

    @classmethod
    def build_url(cls):
        return {f'authorization': f"Bearer {_airtableconfig['API_KEY']}"
                }

    @classmethod
    def build_header(cls):
        return {f'https://api.airtable.com/v0/{_airtableconfig["TABLE_KEY"]}/{_airtableconfig["TABLE_NAME"]}'}


class AirTable:
    def __getattr__(self, name):
        """
        called when getattr(self, name) is not found
        :return:
        :rtype:
        """
        default = partial(self.default, name)
        return default

    def raw(self, params):
        try:
            post(**params)
        except Exception as error:
            raise Exception("Exception at airtable params\n"
                            f"{params}"
                            f"Exception value:"
                            f"{error}")

    def default(self, method, payload):
        raise NotImplemented