from typing import List
from .utils import ResponseContainer
from .route_airtable import AirTable
from .route_slack import Slack, SlackStart
import sys

# ResponseContainer = NamedTuple('ResponseContainer', [('call_class', str), ('call_method', str), ('response', dict)])

def external_router(calls: List[ResponseContainer]):
    # slack, or airtable
    for call in calls:
        cls = getattr(sys.modules[__name__], call.route)()

        class_method = getattr(cls, call.method)
        yield class_method(call.payload)



print(__name__)
if __name__ == '__main__':


    part_one = ResponseContainer(route='Slack', method='chat.update', payload=dict(cat='dog'))

    #SlackStart(api_key='test', verification_token='test')

    part_two = ResponseContainer(route='Slack', method='user_name_from_id', payload=dict(mike='mike'))
    external_router([part_one, part_two ])