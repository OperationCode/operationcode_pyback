from typing import List
from time import time
from ocbot.external.route_slack import SlackBuilder

from .abc import RouteHandler
from ocbot.pipeline.utils import get_response_type


class GreetedHandler(RouteHandler):
    """
    Handles the interactive message sent to the #community channel
    when a new member joins.

    Displays the user that claimed the greeting along with the option
    to un-claim
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
        if click_type == 'greeted':
            params['attachments'] = self.was_greeted_response_attachments()
        else:
            params['attachments'] = self.not_greeted_attachments()

        self.text_dict['message'] = params

    def build_responses(self):
        params = self.text_dict['message']

        self.include_resp(SlackBuilder.update, **params)

    def now(self):
        """
        This has to be pulled out into its own method so a mock can
        be injected for testing purposes
        """
        return int(time())

    def was_greeted_response_attachments(self) -> List[dict]:
        unix_time = self.now()
        return [
            {
                "text": f":100:<@{self._user_id}> has greeted the new user!:100:\n"
                        f"<!date^{unix_time}^Greeted at {{date_num}} {{time_secs}}|Failed to parse time>",
                "fallback": "",
                "color": "#3AA3E3",
                "callback_id": "greeted",
                "attachment_type": "default",
                "actions": [{
                    "name": "reset_greet",
                    "text": f"Reset claim",
                    "type": "button",
                    "style": "danger",
                    "value": "reset_greet",
                }]
            }
        ]

    @staticmethod
    def not_greeted_attachments() -> List[dict]:
        return [
            {
                'text': "",
                "fallback": "I will greet them!",
                "color": "#3AA3E3",
                "callback_id": "greeted",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "greeted",
                        "text": "I will greet them!",
                        "type": "button",
                        "style": "primary",
                        "value": "greeted",
                    },
                ]
            }
        ]

    def make_base_params(self):
        return {
            'text': self._event['original_message']['text'],
            'channel': self._event['channel']['id'],
            'ts': self._event['message_ts'],
            'as_user': True
        }
