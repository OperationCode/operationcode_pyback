import logging

from src import builders as bot

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
        'greeting_buttons': bot.help_menu_interaction,
        'greeted_interaction': bot.greeted_interaction,
        'suggestion_modal': bot.suggestion_submission,
        'mentor_request': bot.mentor_submission,
        'team_join': bot.new_member
    }

    # verify we have event response and we have a handler for it
    if event and json_data[event]['type'] in route_dict.keys():
        route_dict.get(json_data[event]['type'])(json_data)

    # verify we have callback_id response and have handler for it
    if callback_id and json_data[callback_id] in route_dict.keys():
        route_dict.get(json_data[callback_id])(json_data)

    test_route_handler(json_data)


def test_route_handler(json_data):
    if 'event' in json_data.keys() and json_data['event']['type'] == 'message' and 'user' in json_data[
            'event'].keys() and json_data['event']['text'] == 'test':
        data = json_data['event']
        data['user'] = {'id': data['user']}
        bot.new_member(data)
