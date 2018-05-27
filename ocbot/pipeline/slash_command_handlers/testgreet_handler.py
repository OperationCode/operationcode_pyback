from functools import lru_cache

from ocbot.database.models import User


def create_testgreet_event(request):
    event_dict = {
        'event': {
            'user': {
                'id': request['user_id']
            },
            'type': 'team_join',
            'channel_id': request['channel_id'],
        }
    }

    return event_dict


# @lru_cache(100)
def can_test(user_id: str):
    return bool(User.query.filter_by(slack_id=user_id, can_test=True).first())
