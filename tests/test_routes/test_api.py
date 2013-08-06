# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
from tests.utils import MockHttp
from helpers import google_api
import main # The app

class TestAPIHandler(unittest.TestCase):

    # Helper method to test generic error responses
    def denied_authentication(self, response, code=404):
        self.assertEqual(response.status_int, code)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertEqual('error', data['response'])


    def test_api_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api')
        self.denied_authentication(response)


    def test_api_0_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0')
        self.denied_authentication(response)


    def test_api_0_user_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/user')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/user', method='POST')
        self.denied_authentication(response, 403)


    def test_api_0_data_source_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/data_source')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source',method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1', method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1', method='DELETE')
        self.denied_authentication(response, 403)


    def test_api_0_data_view_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/data_source/1/view')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view', method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0', method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0', method='DELETE')
        self.denied_authentication(response, 403)


    def test_api_0_google_sheets_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/google/sheets')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets', method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/0')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/0', method='POST')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/0/0')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/0/0', method='POST')
        self.denied_authentication(response, 403)


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
