# -*- coding: utf-8 -*-

import unittest
import webapp2
from tests.utils import MockHttp
from google.appengine.ext import db
from google.appengine.ext import testbed
from helpers import google_api
import main # The app

class TestSessionHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_login_path_redirects_to_google_auth_endpoint(self):
        response = main.app.get_response('/auth/login')
        self.assertEqual(response.status_int, 302)
        self.assertIn('Location', response.headers)
        self.assertIn('accounts.google.com', response.headers['Location'])

    def test_logout_path_responds(self):
        response = main.app.get_response('/auth/logout')
        self.assertEqual(response.status_int, 302)

    def test_oauth2callback_path_fails_without_code(self):
        response = main.app.get_response('/auth/oauth2callback')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, 'No authentication code returned')

    def test_oauth2callback_path_succeeds_with_code(self):
        # Use mock http client in gogole wrappers
        google_api.httplib2.Http = MockHttp
        
        response = main.app.get_response('/auth/oauth2callback?code=abc123')
        self.assertEqual(response.status_int, 302)
        self.assertTrue('Location' in response.headers)
        self.assertTrue('http://localhost/' in response.headers['Location'])