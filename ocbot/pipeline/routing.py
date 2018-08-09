import logging

from ocbot.pipeline.handlers.airtable_request_handler import NewAirtableRequestHandler
from ocbot.pipeline.handlers.claim_mentee import MenteeClaimHandler
from .handlers.actionmenu import ActionMenuHandler
from .handlers.greeted import GreetedHandler
from .handlers.suggestion import SuggestionHandler
from .handlers.mentor_request import MentorRequestHandler
from .handlers.newmember import NewMemberHandler
from .handlers.testing_handlers import DefaultHandler

logger = logging.getLogger(__name__)


def RoutingHandler(json_data: dict, route_id: str=None) -> None:
    """
        Receved json response data from slack api and uses route dictionary {string: method}
        to direct to the correct method.
        :param json_data: dict
        :param route_id: str
        :returns response: dict
        """
    route_dict = {
        'resource_buttons': ActionMenuHandler,
        'suggestion': ActionMenuHandler,
        'greeted': GreetedHandler,
        'mentor_request': MentorRequestHandler,
        'team_join': NewMemberHandler,
        'suggestion_modal': SuggestionHandler,
        'new_airtable_request': NewAirtableRequestHandler,
        'claim_mentee': MenteeClaimHandler,
    }
    try:
        class_route = route_dict.get(route_id, DefaultHandler)
        handler = class_route(event_dict=json_data)
        handler.event_route()

    except KeyError as error:
        logger.log(logging.WARN, f'Key Error.  Error: {error}.  Executing class: {class_route}')
