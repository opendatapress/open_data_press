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

        drive_files = google_api.list_drive_files(USER_AUTH_JSON)
        self.assertIsInstance(drive_files, dict)
        self.assertTrue('num_files' in drive_files)
        self.assertTrue('files' in drive_files)