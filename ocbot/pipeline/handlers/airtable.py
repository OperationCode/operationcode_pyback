from ocbot.external.route_slack import SlackBuilder, Slack
from ocbot.keys import COMMUNITY_CHANNEL
from ocbot.pipeline.handlers.abc import RouteHandler


class NewAirtableRequestHandler(RouteHandler):

    def __init__(self, *, event_dict):
        self._user_email = event_dict['Email']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        self.api_dict['id'] = Slack().user_id_from_email(self._user_email)

    def database_calls(self):
        pass

    def build_templates(self):
        self.text_dict['message'] = f"User <@{self.api_dict['id']}> " \
                                    f"has requested a mentor\n\nHere's everything!\n {self._event}"

    def build_responses(self):
        message_text = self.text_dict['message']

        self.include_resp(SlackBuilder.message, COMMUNITY_CHANNEL, text=message_text)
