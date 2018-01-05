import ocbot
from ocbot.pipeline.routing import RoutingHandler
from tests.test_data import CALLBACK_GENERIC, NEW_MEMBER


# validates the correct route called for combined_route_director
# validates called with correct data
def test_greeting_buttons_called(mocker):
    """
    Asserts the input dictionary is routed to the correct builder function
    """
    data = CALLBACK_GENERIC
    data['callback_id'] = 'greeting_buttons'
    mocker.patch('ocbot.pipeline.routing.ActionMenuHandler')

    RoutingHandler(data, route_id='resource_buttons')

    assert ocbot.pipeline.routing.ActionMenuHandler.called_with(event_dict=data)


def test_greeted_called(mocker):
    """
    Asserts the input dictionary is routed to the correct builder function
    """
    data = CALLBACK_GENERIC
    data['callback_id'] = 'greeted_interaction'
    mocker.patch('ocbot.pipeline.routing.GreetedHandler')

    RoutingHandler(data, route_id='resource_buttons')

    assert ocbot.pipeline.routing.GreetedHandler.called_with(event_dict=data)


def test_suggestion_modal_called(mocker):
    """
    Asserts the input dictionary is routed to the correct builder function
    """
    data = CALLBACK_GENERIC
    data['callback_id'] = 'suggestion_modal'
    mocker.patch('ocbot.pipeline.routing.SuggestionHandler')

    RoutingHandler(data, route_id='suggestion_modal')

    assert ocbot.pipeline.routing.SuggestionHandler.called_with(event_dict=data)


def test_mentor_request_called(mocker):
    """
    Asserts the input dictionary is routed to the correct builder function
    """
    data = CALLBACK_GENERIC
    data['callback_id'] = 'mentor_request'
    mocker.patch('ocbot.pipeline.routing.MentorRequestHandler')

    RoutingHandler(data, route_id='mentor_request')

    assert ocbot.pipeline.routing.MentorRequestHandler.called_with(event_dict=data)


def test_team_join(mocker):
    """
    Asserts the input dictionary is routed to the correct builder function
    """
    data = NEW_MEMBER
    data['event'] = {'type': 'team_join'}
    mocker.patch('ocbot.pipeline.routing.NewMemberHandler')

    RoutingHandler(data, route_id='team_join')

    assert ocbot.pipeline.routing.NewMemberHandler.called_with(event_dict=data)
