import logging
from .handlers.actionmenu import ActionMenuHandler
from .handlers.greeted import GreetedHandler
from .handlers.suggestion import SuggestionHandler
from .handlers.mentor_request import MentorRequestHandler
from .handlers.newmember import NewMemberHandler


logger = logging.getLogger(__name__)


def combined_route_director(json_data: dict, event=None, callback_id=None) -> None:
    """
        Receved json response data from slack api and uses route dictionary {string: method}
        to direct to the correct method.
        :param json_data: dict
        :param required_key: str
        :returns response: dict
        """
    route_dict = {
        'greeting_buttons': ActionMenuHandler,
        'greeted_interaction': GreetedHandler,
        'suggestion_modal': SuggestionHandler,
        'mentor_request': MentorRequestHandler,
        'team_join': NewMemberHandler
    }

    # verify we have event response and we have a handler for it

    if event and json_data[event]['type'] in route_dict.keys():
        class_route = route_dict.get(json_data[event]['type'])
        class_route(event_dict=json_data)
    # verify we have callback_id response and have handler for it
    if callback_id and json_data[callback_id] in route_dict.keys():
        route_dict.get(json_data[callback_id])(event_dict=json_data)

    #test_route_handler(json_data)


# def test_route_handler(json_data):
#     if 'event' in json_data.keys() and json_data['event']['type'] == 'message' and 'user' in json_data[
#             'event'].keys() and json_data['event']['text'] == 'test':
#         data = json_data['event']
#         data['user'] = {'id': data['user']}
#         bot.new_member(data)
#
# ActionMenuHandler(test)