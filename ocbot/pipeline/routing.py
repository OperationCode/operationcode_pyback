import logging
from .handlers.actionmenu import ActionMenuHandler
from .handlers.greeted import GreetedHandler
from .handlers.suggestion import SuggestionHandler
from .handlers.mentor_request import MentorRequestHandler
from .handlers.newmember import NewMemberHandler
from .handlers.testing_handlers import test_message_handler, DefaultHandler

logger = logging.getLogger(__name__)


def RoutingHandler(json_data: dict, route_id=None) -> None:
    """
        Receved json response data from slack api and uses route dictionary {string: method}
        to direct to the correct method.
        :param json_data: dict
        :param route_id: str
        :returns response: dict
        """
    route_dict = {
        'greeting_buttons': ActionMenuHandler,
        'greeted': GreetedHandler,
        'suggestion_modal': SuggestionHandler,
        'mentor_request': MentorRequestHandler,
        'team_join': NewMemberHandler,
    }
    try:
        class_route = route_dict.get(route_id, test_message_handler)
        handler = class_route(event_dict=json_data)
        handler.event_route()

    except KeyError as error:
        pass

    #test_route_handler(json_data)


# def test_route_handler(json_data):
#     if 'event' in json_data.keys() and json_data['event']['type'] == 'message' and 'user' in json_data[
#             'event'].keys() and json_data['event']['text'] == 'test':
#         data = json_data['event']
#         data['user'] = {'id': data['user']}
#         bot.new_member(data)
#
# ActionMenuHandler(test)