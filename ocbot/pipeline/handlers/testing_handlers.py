from ocbot.pipeline.handlers.abc import RouteHandler
from .newmember import NewMemberHandler


class DefaultHandler(RouteHandler):
    def __init__(self, *, event_dict):
        self._event = event_dict
        super().__init__()

    def event_route(self):
        pass

    def api_calls(self):
        pass

    def build_responses(self):
        pass

    def database_calls(self):
        pass

    def build_templates(self):
        pass


def test_message_handler(*, event_dict):
    if 'text' in event_dict['event'] and event_dict['event']['text'] == 'testgreet':
        event_dict['event']['user'] = {
                "id": event_dict['event']['user']
            }

        return NewMemberHandler(event_dict=event_dict)
    else:
        return DefaultHandler(event_dict=event_dict)
