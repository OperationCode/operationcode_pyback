import unittest

import mock

from ocbot.web.routing_interface import combined_route_director
from tests.test_data import CALLBACK_GENERIC, NEW_MEMBER


class ValidateDecorator(unittest.TestCase):
    @mock.patch('src.builders.help_menu_interaction')
    def test_greeting_buttons_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'greeting_buttons'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(data)

    @mock.patch('src.builders.greeted_interaction')
    def test_greeted_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'greeted_interaction'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(data)

    @mock.patch('src.builders.suggestion_submission')
    def test_suggestion_modal_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'suggestion_modal'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(data)

    @mock.patch('src.builders.mentor_submission')
    def test_mentor_request_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = CALLBACK_GENERIC
        data['callback_id'] = 'mentor_request'
        combined_route_director(data, callback_id='callback_id')
        mock_func_call.assert_called_with(data)

    @mock.patch('src.builders.new_member')
    def test_team_join(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        data = NEW_MEMBER
        data['event'] = {'type':'team_join'}
        combined_route_director(data, event='event')
        mock_func_call.assert_called_with(data)