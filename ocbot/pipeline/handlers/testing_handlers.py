from ocbot.pipeline.handlers.abc import RouteHandler


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
        return DefaultHandler(event_dict=event_dict)