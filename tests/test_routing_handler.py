import unittest

import mock


from ocbot.pipeline.routing import combined_route_director

from tests.test_data import CALLBACK_GENERIC, NEW_MEMBER

# validates the correct route called
# validates called with correct data
class ValidateRoutingCall(unittest.TestCase):
    @mock.patch('ocbot.pipeline.routing.ActionMenuHandler')
    def test_greeting_buttons_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'greeting_buttons'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(event_dict=data)

    @mock.patch('ocbot.pipeline.routing.GreetedHandler')
    def test_greeted_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'greeted_interaction'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(event_dict=data)

    @mock.patch('ocbot.pipeline.routing.SuggestionHandler')
    def test_suggestion_modal_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'suggestion_modal'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(event_dict=data)

    @mock.patch('ocbot.pipeline.routing.MentorRequestHandler')
    def test_mentor_request_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'mentor_request'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(event_dict=data)

    @mock.patch('ocbot.pipeline.routing.NewMemberHandler')
    def test_team_join(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = NEW_MEMBER
        data['event'] = {'type':'team_join'}
        combined_route_director(data, event='event')
        mock_func_call.assert_called_with(event_dict=data)