import logging

from src import builders as bot

logger = logging.getLogger(__name__)
new_event_logger = logging.getLogger(f'{__name__}.new_member')


def combined_route_director(json_data: dict, required_key: str) -> None:
    """
        Receved json response data from slack api and uses route dictionary {string: method}
        to direct to the correct method.
        :param json_data: dict
        :param required_key: str
        :returns response: dict
        """
    route_dict = {
        'greeting_buttons': bot.help_menu_interaction,
        'greeted': bot.greeted_interaction,
        'suggestion_modal': bot.suggestion_submission,
        'mentor_request': bot.mentor_submission,
        'team_join': bot.new_member
    }

    if json_data[required_key] in route_dict.keys():
        route_dict.get(json_data[required_key])(json_data)

    test_route_handler(json_data)


def test_route_handler(json_data):
    if json_data['type'] is 'message' and \
                    'user' in json_data.keys() and \
                    json_data['text'] is 'testgreet':
        json_data['user'] = {'id': json_data['user']}
        bot.new_member(json_data)
