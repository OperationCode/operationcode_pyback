from .abc import RouteHandler
from ocbot.external.route_airtable import AirTableBuilder


class MentorRequestHandler(RouteHandler):
    """
        Parses the mentor request dialog form and pushes the data to Airtable.
        :param event_dict : dict
        :return response: Response
    """

    def __init__(self, *, event_dict):
        self.user_id = event_dict['user']['id']
        self._event = event_dict
        super().__init__()

    # TODO stop mocking api call, switch to actual api call
    def api_calls(self):
        # get static table name instead of api call
        self.api_dict['service'] = AirTableBuilder.record(self._event['submission']['service'])

    def database_calls(self):
        pass

    def build_templates(self):
        form = self._event['submission']

        self.text_dict['params'] = {
            'fields': {
                'Slack User': form['Slack User'],
                'Email': form['Email'],
                'Service': [self.api_dict['service']],
                'Skillsets': [form['skillset']],
                'Additional Details': form['Additional Details']
            }
        }

    def build_responses(self):
        params = self.text_dict['params']
        self.include_resp(AirTableBuilder.entry, params)
