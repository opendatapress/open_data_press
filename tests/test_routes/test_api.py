# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
from tests.utils import MockHttp
from google.appengine.ext import db
from google.appengine.ext import testbed
from helpers import google_api
import main # The app

class TestAPIHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    # Helper method to test generic error responses
    def denied_authentication(self, response, code=404):
        self.assertEqual(response.status_int, code)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertTrue('body' in data)
        self.assertEqual('error', data['response'])

    # Helper method to test successful response
    def response_ok(self, response):
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)
        data = json.loads(response.body)
        self.assertTrue('response' in data)
        self.assertTrue('body' in data)



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


    def test_api_0_user_get_returns_user_data(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/user', headers=headers)

        self.response_ok(response)
        data = json.loads(response.body)
        self.assertEqual("12345", data["body"]["google_id"])


    def test_api_0_user_post_updates_user_data(self):
        google_api.httplib2.Http = MockHttp
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}

        # Get user data
        response_a = main.app.get_response('/api/0/user', headers=headers)
        self.response_ok(response_a)

        # Modify user
        user_data_a = json.loads(response_a.body)["body"]
        user_data_a["profile_description"]   = "New description"
        user_data_a["profile_web_address"]   = "http://new_web_address.com"
        user_data_a["profile_email"]         = "new@email.com"
        user_data_a["profile_name"]          = "New Name"

        # Attempt to save the modified user
        response_b = main.app.get_response('/api/0/user', headers=headers, POST={"payload":json.dumps(user_data_a)})
        self.response_ok(response_b)

        # Assert returned data is correct
        user_data_b = json.loads(response_b.body)["body"]
        self.assertEqual(user_data_b["profile_description"], "New description")
        self.assertEqual(user_data_b["profile_web_address"], "http://new_web_address.com")
        self.assertEqual(user_data_b["profile_email"],       "new@email.com")
        self.assertEqual(user_data_b["profile_name"],        "New Name")


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
        
        response = main.app.get_response('/api/0/google/sheets/abc123')
        self.denied_authentication(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/abc123/abc123')
        self.denied_authentication(response, 403)
        

    def test_api_0_get_google_sheets_list(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets', headers=headers)

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_worksheets(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/dummy_key', headers=headers)

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_worksheets_not_found(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/not_found', headers=headers)

        self.assertEqual(response.status_int, 500)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_worksheets_bad_format(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/bad_format', headers=headers)

        self.assertEqual(response.status_int, 500)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_cells(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/dummy_key/dummy_id', headers=headers)

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_cells_not_found(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/dummy_key/not_found', headers=headers)

        self.assertEqual(response.status_int, 500)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)

    def test_api_0_get_google_sheets_cells_bad_format(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/api/0/google/sheets/dummy_key/bad_format', headers=headers)

        self.assertEqual(response.status_int, 500)
        self.assertEqual(response.content_type, 'application/json')
        # NB response content tested in helpers/test_google_api.py
        self.assertIsInstance(json.loads(response.body), dict)