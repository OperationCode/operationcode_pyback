from nose.tools import assert_equal
import unittest
from mock import Mock, MagicMock, patch


from src.route_decorators import validate_response, url_verification
from utils.keys import VERIFICATION_TOKEN, COMMUNITY_CHANNEL, AIRTABLE_API_KEY

class RoutingInterface(unittest.TestCase):

    @patch("json.loads", MagicMock(return_value=VERIFICATION_TOKEN))
    def test_validated_token_one(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """

        func = Mock(return_value='good response')
        wrapping_func = url_verification(func)

        decorator_params = ('token', VERIFICATION_TOKEN)

        response = wrapping_func(decorator_params)
        func.assert_called_with(decorator_params)
        assert_equal(response, 'good response')


    def test_validated_community_channel(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        func = Mock(return_value='my response')
        decorated_func = url_verification(func)
        request = prepare_request_with_ok_user()
        response = decorated_func(request)
        func.assert_called_with(request)
        assert_equal(response, 'my response')

    def test_validated_airtable_key(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        func = Mock(return_value='my response')

        decorated_func = url_verification(func)
        request = prepare_request_with_ok_user()
        response = decorated_func(request)
        func.assert_called_with(request)
        assert_equal(response, 'my response')


    @mock.patch('src.builders.mentor_submission')
    def test_not_validated_token(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        func = Mock()
        decorated_func = url_verification(func)
        request = prepare_request_without_user()
        response = decorated_func(request)
        assert not func.called
        # assert response is redirect

    @mock.patch('src.builders.new_member')
    def test_not_validated_community_channel(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        func = Mock()
        decorated_func = url_verification(func)
        request = prepare_request_without_user()
        response = decorated_func(request)
        assert not func.called
        # assert response is redirect

    @mock.patch('src.builders.new_member')
    def test_not_validated_airtable_key(self, mock_func_call):
        """
        Asserts the input dictionary is routed to the correct builder function
        """
        func = Mock()
        decorated_func = url_verification(func)
        request = prepare_request_without_user()
        response = decorated_func(request)
        assert not func.called
        # assert response is redirect