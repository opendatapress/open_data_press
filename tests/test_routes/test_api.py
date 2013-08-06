# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
from tests.utils import MockHttp
from helpers import google_api
import main # The app

USER_AUTH_JSON="""
{
    "access_token":  "XXX",
    "client_id":     "XXX",
    "client_secret": "XXX",
    "refresh_token": "XXX",
    "token_expiry":  "2015-00-00T00:00:00Z",
    "token_uri":     "http://example.com",
    "user_agent":    "XXX",
    "invalid":       "XXX"
}
"""

class TestAPIHandler(unittest.TestCase):

    def test_api_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api')
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0')
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_user_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/user')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/user', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_data_source_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/data_source')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source',method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1', method='DELETE')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_data_view_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/data_source/1/view')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1/view', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1/view/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1/view/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/data_source/1/view/0', method='DELETE')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_google_sheets_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/google/sheets')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/google/sheets', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/google/sheets/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/google/sheets/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/google/sheets/0/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])

        response = main.app.get_response('/api/0/google/sheets/0/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_0_get_google_sheets_list(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets', headers=headers)

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        # Parse response
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('success', data['response'])
        self.assertTrue('body' in data)
        self.assertTrue('files' in data['body'])
        self.assertTrue('num_files' in data['body'])
