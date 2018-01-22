from ocbot.external.route_slack import SlackBuilder, Slack
from ocbot.keys import COMMUNITY_CHANNEL
from .abc import RouteHandler
from ocbot.pipeline.utils import needs_greet_button
from ocbot.database.pybotdatabase import PyBotDatabase


class FrontendChatHandler(RouteHandler):

    def __init__(self, *, event_dict):
        self.user_id = event_dict['email']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        pass

    def database_calls(self):
        db = PyBotDatabase()
        # db._remake_tables()
        # db._populate_interests()
        db_res = db.get_chat_session(self.user_id)
        if db_res:
            self._event['thread_ts'] = db_res['thread_ts']
            self.api_dict['thread_ts'] = Slack().post_to_chat_thread(self._event['message'], db_res['thread_ts'])
        else:
            self.api_dict['thread_ts'] = Slack().post_new_frontend_chat_message(self._event['message'], self.user_id)
            self._event['thread_ts'] = self.api_dict['thread_ts']
            self.db_dict['db_res'] = db.add_chat_session(email=self._event['email'], thread_ts=self._event['thread_ts'])

    def process_db_response(self):
        pass

    def build_templates(self):
        pass

    def build_responses(self):
        pass
