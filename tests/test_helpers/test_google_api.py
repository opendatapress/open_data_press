# -*- coding: utf-8 -*-
import os
import unittest
from helpers import google_api
from oauth2client.client import OAuth2WebServerFlow
from tests.utils import MockHttp


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

class GoogleAPITest(unittest.TestCase):

    def test_oauth2_flow(self):
        flow = google_api.oauth2_flow()
        self.assertIsInstance(flow, OAuth2WebServerFlow)

    def test_http_from_oauth2(self):
        self.assertIn('http_from_oauth2', dir(google_api))

    def test_user_info(self):
        google_api.httplib2.Http = MockHttp
        self.assertIn('user_info', dir(google_api))
        
        user_info = google_api.user_info(USER_AUTH_JSON)
        self.assertIsInstance(user_info, dict)

    def test_drive_service(self):
        self.assertIn('drive_service', dir(google_api))

    def test_list_drive_files(self):
        google_api.httplib2.Http = MockHttp
        self.assertIn('list_drive_files', dir(google_api))

        data = google_api.list_drive_files(USER_AUTH_JSON)
        self.assertIsInstance(data, dict)
        self.assertTrue('response'  in data)
        self.assertTrue('body'      in data)
        self.assertTrue('num_files' in data['body'])
        self.assertTrue('files'     in data['body'])
        self.assertEqual('success', data['response'])

    def test_get_worksheets_success(self):
        google_api.httplib2.Http = MockHttp
        self.assertIn('get_worksheets', dir(google_api))

        data = google_api.get_worksheets(USER_AUTH_JSON, 'dummy_key')
        self.assertIsInstance(data, dict)
        self.assertTrue('response'      in data)
        self.assertTrue('body'          in data)
        self.assertTrue('key'           in data['body'])
        self.assertTrue('title'         in data['body'])
        self.assertTrue('updated'       in data['body'])
        self.assertTrue('total_results' in data['body'])
        self.assertTrue('start_index'   in data['body'])
        self.assertTrue('author'        in data['body'])
        self.assertTrue('worksheets'    in data['body'])
        self.assertTrue('name'          in data['body']['author'])
        self.assertTrue('email'         in data['body']['author'])
        self.assertEqual('success', data['response'])

    def test_get_worksheets_not_found(self):
        google_api.httplib2.Http = MockHttp
        data = google_api.get_worksheets(USER_AUTH_JSON, 'not_found')
        self.assertIsInstance(data, dict)
        self.assertTrue('response' in data)
        self.assertTrue('body'     in data)
        self.assertEqual('error',  data['response'])    

    def test_get_worksheets_bad_format(self):
        google_api.httplib2.Http = MockHttp
        data = google_api.get_worksheets(USER_AUTH_JSON, 'bad_format')
        self.assertIsInstance(data, dict)
        self.assertTrue('response' in data)
        self.assertTrue('body'     in data)
        self.assertEqual('error',  data['response'])    

    def test_get_cell_data(self):
        google_api.httplib2.Http = MockHttp
        self.assertIn('get_cell_data', dir(google_api))

        data = google_api.get_cell_data(USER_AUTH_JSON, 'dummy_key', 'dummy_id')
        self.assertIsInstance(data, dict)
        self.assertTrue('response'        in data)
        self.assertEqual('success', data['response'])

        self.assertTrue('body'            in data)
        self.assertTrue('spreadsheet_key' in data['body'])
        self.assertTrue('worksheet_key'   in data['body'])
        self.assertTrue('title'           in data['body'])
        self.assertTrue('updated'         in data['body'])
        self.assertTrue('total_results'   in data['body'])
        self.assertTrue('start_index'     in data['body'])
        self.assertTrue('data_rows'       in data['body'])

        self.assertTrue('author'          in data['body'])
        self.assertTrue('name'            in data['body']['author'])
        self.assertTrue('email'           in data['body']['author'])

    def test_get_cell_data_not_found(self):
        google_api.httplib2.Http = MockHttp
        data = google_api.get_cell_data(USER_AUTH_JSON, 'dummy_key', 'not_found')
        self.assertIsInstance(data, dict)
        self.assertTrue('response'  in data)
        self.assertTrue('body'      in data)
        self.assertEqual('error',   data['response'])

    def test_get_cell_data_bad_format(self):
        google_api.httplib2.Http = MockHttp
        data = google_api.get_cell_data(USER_AUTH_JSON, 'dummy_key', 'bad_format')
        self.assertIsInstance(data, dict)
        self.assertTrue('response'  in data)
        self.assertTrue('body'      in data)
        self.assertEqual('error',   data['response'])

    def test_create_spreadsheet(self):
        self.assertIn('create_spreadsheet', dir(google_api))

    def test_create_worksheet(self):
        self.assertIn('create_worksheet', dir(google_api))

    def test_save_data(self):
        self.assertIn('save_data', dir(google_api))