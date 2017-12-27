#!flask/bin/python
import json
import unittest

from mock import patch

from keys import VERIFICATION_TOKEN
from src.app import app
from tests.test_data import CHALLENGE, NEW_MEMBER


class RequestVerification(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('src.app.combined_route_director')
    def test_good_slack_token(self, mock):
        data = NEW_MEMBER
        data['token'] = VERIFICATION_TOKEN
        json_data = json.dumps(data)
        response = self.app.post('/event_endpoint', data=json_data,
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertTrue(mock.called)
        self.assertEqual(response.status_code, 200)

    @patch('src.app.combined_route_director')
    def test_bad_slack_token(self, mock):
        data = NEW_MEMBER
        data['token'] = 'bad token'
        json_data = json.dumps(data)
        response = self.app.post('/event_endpoint', data=json_data,
                                 content_type='application/json',
                                 follow_redirects=True)

        self.assertFalse(mock.called)
        self.assertEqual(response.status_code, 403)

    @patch('src.app.combined_route_director')
    def test_empty_slack_value_token(self, mock):
        data = NEW_MEMBER
        data['token'] = None
        json_data = json.dumps(data)
        response = self.app.post('/event_endpoint', data=json_data,
                                 content_type='application/json',
                                 follow_redirects=True)


        self.assertFalse(mock.called)

        self.assertEqual(response.status_code, 403)

    @patch('src.app.combined_route_director')
    def test_empty_token_slack_data(self, mock):
        response = self.app.post('/event_endpoint', data=None,
                                 content_type='application/json',
                                 follow_redirects=True)

        self.assertFalse(mock.called)
        self.assertEqual(response.status_code, 400)

class ChallengeVerification(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('src.app.combined_route_director')
    def test_challenge_redirect(self, mock):
        '''
        :param mock: combined_route_director, don't want to call function
        :return:
        This case tests if we have a verification token
        '''
        CHALLENGE['token'] = VERIFICATION_TOKEN
        data = json.dumps(CHALLENGE)
        response = self.app.post('/event_endpoint', data=data,
                                 content_type='application/json',
                                 follow_redirects=True)
        self.assertFalse(mock.called)
        self.assertEqual(response.status_code, 200)


    @patch('src.app.combined_route_director')
    @patch('src.app.validate_response')
    def test_url_verified_called(self, validate_deco, route_mock ):
        '''
        :param mock: combined_route_director, don't want to call function
        :return:
        This case tests if we have a verification token
        '''
        CHALLENGE['token'] = VERIFICATION_TOKEN
        data = json.dumps(CHALLENGE)
        response = self.app.post('/event_endpoint', data=data,
                                 content_type='application/json',
                                 follow_redirects=True)

        self.assertFalse(validate_deco.called)
        self.assertFalse(route_mock.called)
        self.assertEqual(response.status_code, 200)


