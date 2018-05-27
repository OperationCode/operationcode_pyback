from typing import List
from ocbot.external import ResponseContainer
from .route_airtable import Airtable
from .route_slack import Slack
import sys


# ResponseContainer = NamedTuple('ResponseContainer', [('call_class', str), ('call_method', str), ('response', dict)])

def external_router(calls: List[ResponseContainer]):
    # slack, or airtable
    for call in calls:
        cls = getattr(sys.modules[__name__], call.route)()
        class_method = getattr(cls, call.method)
        class_method(call.payload)
