# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
from tests.utils import MockHttp
from tests import dummy
from google.appengine.ext import db
from google.appengine.ext import testbed
from helpers import google_api
from models.data_source import DataSource
import main # The app

class TestAPIHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        # Get headers for making authenticated requests
        google_api.httplib2.Http = MockHttp
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        self.auth_headers  = {'Cookie': response.headers['Set-Cookie']}

        # Create Data Source to use in tests
        ds = DataSource(**dummy.data_source)
        ds.put()
        self.ds_id = ds.key().id()


    def tearDown(self):
        self.testbed.deactivate()


    # Helper method to test generic error responses
    def response_error(self, response, code=404):
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
        self.assertEqual('success', data['response'])



    def test_api_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api')
        self.response_error(response)


    def test_api_0_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0')
        self.response_error(response)


    def test_api_0_user_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/user')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/user', method='POST')
        self.response_error(response, 403)


    def test_api_0_user_get_returns_user_data(self):
        
        response = main.app.get_response('/api/0/user', headers=self.auth_headers)

        self.response_ok(response)
        data = json.loads(response.body)
        self.assertEqual("12345", data["body"]["google_id"])


    def test_api_0_user_post_updates_user_data(self):
        # Get user data
        response_a = main.app.get_response('/api/0/user', headers=self.auth_headers)
        self.response_ok(response_a)

        # Modify user
        user_data_a = json.loads(response_a.body)["body"]
        user_data_a["profile_description"]   = "New description"
        user_data_a["profile_web_address"]   = "http://new_web_address.com"
        user_data_a["profile_email"]         = "new@email.com"
        user_data_a["profile_name"]          = "New Name"

        # Attempt to save the modified user
        response_b = main.app.get_response('/api/0/user', headers=self.auth_headers, POST={"payload":json.dumps(user_data_a)})
        self.response_ok(response_b)

        # Assert returned data is correct
        user_data_b = json.loads(response_b.body)["body"]
        self.assertEqual(user_data_b["profile_description"], "New description")
        self.assertEqual(user_data_b["profile_web_address"], "http://new_web_address.com")
        self.assertEqual(user_data_b["profile_email"],       "new@email.com")
        self.assertEqual(user_data_b["profile_name"],        "New Name")


    def test_api_0_data_source_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/data_source')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source',method='POST')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1', method='POST')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1', method='DELETE')
        self.response_error(response, 403)


    def test_api_0_data_source_list_all(self):
        response = main.app.get_response('/api/0/data_source', headers=self.auth_headers)
        self.response_ok(response)

        data = json.loads(response.body)["body"]
        self.assertTrue('total_results' in data)
        self.assertTrue('data_sources'  in data)


    def test_api_0_data_source_add_item_fail(self):
        payload  = {}
        response = main.app.get_response('/api/0/data_source', headers=self.auth_headers, POST={"payload": json.dumps(payload)})
        self.response_error(response, 500)


    def test_api_0_data_source_add_item(self):
        payload  = {'key':'dummy_key', 'id':'dummy_id', 'title':'My New Open Data'}
        response = main.app.get_response('/api/0/data_source', headers=self.auth_headers, POST={"payload": json.dumps(payload)})
        self.response_ok(response)
        
        data = json.loads(response.body)["body"]
        self.assertTrue('created_at'         in data)
        self.assertTrue('data_views'         in data)
        self.assertTrue('description'        in data)
        self.assertTrue('google_spreadsheet' in data)
        self.assertTrue('google_worksheet'   in data)
        self.assertTrue('id'                 in data)
        self.assertTrue('licence'            in data)
        self.assertTrue('modified_at'        in data)
        self.assertTrue('slug'               in data)
        self.assertTrue('tags'               in data)
        self.assertTrue('tbl_stars'          in data)
        self.assertTrue('title'              in data)

        self.assertEqual(data['google_spreadsheet'], payload['key'])
        self.assertEqual(data['google_worksheet'],   payload['id'])
        self.assertEqual(data['title'],              payload['title'])


    def test_api_0_data_source_get_item_fail(self):
        response = main.app.get_response('/api/0/data_source/not_found', headers=self.auth_headers)
        self.response_error(response)


    def test_api_0_data_source_get_item(self):
        response = main.app.get_response('/api/0/data_source/%s' % self.ds_id, headers=self.auth_headers)
        self.response_ok(response)
        
        data = json.loads(response.body)["body"]
        self.assertTrue('created_at'         in data)
        self.assertTrue('data_views'         in data)
        self.assertTrue('description'        in data)
        self.assertTrue('google_spreadsheet' in data)
        self.assertTrue('google_worksheet'   in data)
        self.assertTrue('id'                 in data)
        self.assertTrue('licence'            in data)
        self.assertTrue('modified_at'        in data)
        self.assertTrue('slug'               in data)
        self.assertTrue('tags'               in data)
        self.assertTrue('tbl_stars'          in data)
        self.assertTrue('title'              in data)
        
        self.assertEqual(data['id'], self.ds_id)


    def test_api_0_data_source_update_item(self):
        payload = dummy.data_source_json
        response = main.app.get_response('/api/0/data_source/%s' % self.ds_id, headers=self.auth_headers, POST={"payload": json.dumps(payload)})
        self.response_ok(response)
        
        data = json.loads(response.body)["body"]
        self.assertTrue('created_at'         in data)
        self.assertTrue('data_views'         in data)
        self.assertTrue('description'        in data)
        self.assertTrue('google_spreadsheet' in data)
        self.assertTrue('google_worksheet'   in data)
        self.assertTrue('id'                 in data)
        self.assertTrue('licence'            in data)
        self.assertTrue('modified_at'        in data)
        self.assertTrue('slug'               in data)
        self.assertTrue('tags'               in data)
        self.assertTrue('tbl_stars'          in data)
        self.assertTrue('title'              in data)

        self.assertEqual(data['created_at'],         payload['created_at'])
        self.assertEqual(data['data_views'],         payload['data_views'])
        self.assertEqual(data['description'],        payload['description'])
        self.assertEqual(data['google_spreadsheet'], payload['google_spreadsheet'])
        self.assertEqual(data['google_worksheet'],   payload['google_worksheet'])
        self.assertEqual(data['id'],                 payload['id'])
        self.assertEqual(data['licence'],            payload['licence'])
        self.assertEqual(data['modified_at'],        payload['modified_at'])
        self.assertEqual(data['slug'],               payload['slug'])
        self.assertEqual(data['tags'],               payload['tags'])
        self.assertEqual(data['tbl_stars'],          payload['tbl_stars'])
        self.assertEqual(data['title'],              payload['title'])


    def test_api_0_data_source_delete_item(self):
        response = main.app.get_response('/api/0/data_source/%s' % self.ds_id, headers=self.auth_headers, method='DELETE')
        self.response_ok(response)


    def test_api_0_data_view_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/data_source/1/view')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view', method='POST')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0', method='POST')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/data_source/1/view/0', method='DELETE')
        self.response_error(response, 403)


    def test_api_0_data_view_list_all(self):
        pass


    def test_api_0_data_view_add_item(self):
        pass


    def test_api_0_data_view_get_item(self):
        pass


    def test_api_0_data_view_update_item(self):
        pass


    def test_api_0_data_view_delete_item(self):
        pass


    def test_api_0_google_sheets_path_denies_unauthenticated_requests(self):
        
        response = main.app.get_response('/api/0/google/sheets')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/abc123')
        self.response_error(response, 403)
        
        response = main.app.get_response('/api/0/google/sheets/abc123/abc123')
        self.response_error(response, 403)
        

    def test_api_0_get_google_sheets_list(self):
        response = main.app.get_response('/api/0/google/sheets', headers=self.auth_headers)
        self.response_ok(response)
        # NB Respose body tested in helpers/test_google_api.py

    def test_api_0_get_google_sheets_worksheets(self):
        response = main.app.get_response('/api/0/google/sheets/dummy_key', headers=self.auth_headers)
        self.response_ok(response)
        # NB Respose body tested in helpers/test_google_api.py

    def test_api_0_get_google_sheets_worksheets_not_found(self):
        response = main.app.get_response('/api/0/google/sheets/not_found', headers=self.auth_headers)
        self.response_error(response, 500)

    def test_api_0_get_google_sheets_worksheets_bad_format(self):
        response = main.app.get_response('/api/0/google/sheets/bad_format', headers=self.auth_headers)
        self.response_error(response, 500)

    def test_api_0_get_google_sheets_cells(self):
        response = main.app.get_response('/api/0/google/sheets/dummy_key/dummy_id', headers=self.auth_headers)
        self.response_ok(response)
        # NB Respose body tested in helpers/test_google_api.py

    def test_api_0_get_google_sheets_cells_not_found(self):
        response = main.app.get_response('/api/0/google/sheets/dummy_key/not_found', headers=self.auth_headers)
        self.response_error(response, 500)

    def test_api_0_get_google_sheets_cells_bad_format(self):
        response = main.app.get_response('/api/0/google/sheets/dummy_key/bad_format', headers=self.auth_headers)
        self.response_error(response, 500)