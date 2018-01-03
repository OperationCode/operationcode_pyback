from ocbot.external.route_slack import SlackBuilder

from ocbot.keys import COMMUNITY_CHANNEL
from .abc import RouteHandler
from ocbot.pipeline.utils import needs_greet_button, get_response_type


class GreetedHandler(RouteHandler):
    """
        Handles the interactive message sent to the #community channel
        when a new member joins.
    """

    def __init__(self, *, event_dict):
        self._user_id = event_dict['user']['id']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        pass

    # TODO have bot look through resources for this item
    # TODO to get additional items
    def database_calls(self):
        pass

    def build_templates(self):
        click_type = get_response_type(self._event)
        params = self.make_base_params()

        # adjust button type
        params['attachments'] = self.was_greeted() if click_type == 'greeted' else needs_greet_button()
        # params['ts'] = self._event['message_ts']
        self.text_dict['message'] = params

    def build_responses(self):
        params = self.text_dict['message']

        self.include_resp(SlackBuilder.update, COMMUNITY_CHANNEL, text=params, ts=params['ts'])

    def was_greeted(self):
        return [
            {
                "text": f":100:<@{self._user_id}> has greeted the new user!:100:",
                "fallback": "",
                "color": "#3AA3E3",
                "callback_id": "greeted",
                "attachment_type": "default",
                "actions": [{
                    "name": "reset_greet",
                    "text": f"Reset {self._user_id}'s claim",
                    "type": "button",
                    "style": "danger",
                    "value": "reset_greet",
                }]
            }
        ]

    def make_base_params(self):
        return {'text': self._event['original_message']['text'],
                'channel': self._event['channel']['id'],
                'ts': self._event['message_ts'],
                'as_user': True
                }
