from ocbot.external.route_airtable import AirTableBuilder
from ocbot.external.route_slack import SlackBuilder, Slack
from ocbot.pipeline.handlers.abc import RouteHandler
from config.configs import configs

MENTORS_INTERNAL_CHANNEL = configs['MENTORS_INTERNAL_CHANNEL']

class NewAirtableRequestHandler(RouteHandler):

    def __init__(self, *, event_dict):
        self._user_email = event_dict['Email']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        """
        Queries slack for user ID to be linked to their account (@user)
        If not found defaults to displaying the provided Slack Username in plaintext
        :return:
        """
        response = Slack().user_id_from_email(self._user_email)
        if response['ok']:
            self.api_dict['user'] = f"<@{response['user']['id']}>"
        else:
            self.api_dict['user'] = self._event['Slack User']

    def database_calls(self):
        pass

    def build_templates(self):
        service = AirTableBuilder.record_to_service(self._event['Service'])
        if 'skillsets' not in self._event:
            self._event['Skillsets'] = 'None given'

        self.text_dict['message'] = f"User {self.api_dict['user']} has requested a mentor for {service}\n\n" \
                                    f"Given Skillset(s): {self._event['Skillsets']}\n\n" \
                                    f"View requests: <https://airtable.com/tbl9uQEE8VeMdNCey/viwYzYa4J9aytVB4B|Airtable>\n\n" \
                                    f"Please reply to the channel if you'd like to be assigned to this request."
        self.text_dict['details'] = f"Additional details: {self._event['Details']}"

    def build_responses(self):
        message_text = self.text_dict['message']
        details_text = self.text_dict['details']

        self.include_resp(SlackBuilder.mentor_request, MENTORS_INTERNAL_CHANNEL, details=details_text,
                          text=message_text)
