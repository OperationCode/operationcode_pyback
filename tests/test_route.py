import unittest
import mock
from src.routing_interface import combined_route_director





class ValidateDecorator(unittest.TestCase):
    @mock.patch('src.builders.help_menu_interaction')
    def test_greeting_buttons_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        mock_dict = {'callback': 'greeting_buttons'}
        combined_route_director(mock_dict, 'callback')
        mock_func_call.assert_called_with(mock_dict)

    @mock.patch('src.builders.greeted_interaction')
    def test_greeted_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        mock_dict = {'callback': 'greeted'}
        combined_route_director(mock_dict, 'callback')
        mock_func_call.assert_called_with(mock_dict)

    @mock.patch('src.builders.suggestion_submission')
    def test_suggestion_modal_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        mock_dict = {'callback': 'suggestion_modal'}
        combined_route_director(mock_dict, 'callback')
        mock_func_call.assert_called_with(mock_dict)

    @mock.patch('src.builders.mentor_submission')
    def test_mentor_request_called(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        mock_dict = {'callback': 'mentor_request'}
        combined_route_director(mock_dict, 'callback')
        mock_func_call.assert_called_with(mock_dict)

    @mock.patch('src.builders.new_member')
    def test_team_join(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        mock_dict = {'event': 'team_join'}
        combined_route_director(mock_dict, 'event')
        mock_func_call.assert_called_with(mock_dict)


