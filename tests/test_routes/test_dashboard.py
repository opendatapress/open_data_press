# -*- coding: utf-8 -*-

import unittest
from tests.utils import MockHttp
from google.appengine.ext import testbed
from helpers import google_api
import main # The app

class TestDashboardHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_dashboard_rejects_unauthenticated_user(self):
        # Make unauthenticated request
        response = main.app.get_response('/dashboard')
        self.assertEqual(response.status_int, 302)
        self.assertTrue('Location' in response.headers)
        self.assertTrue('/auth/login' in response.headers['Location'])

    def test_dashboard_accepts_authenticated_user(self):
        google_api.httplib2.Http = MockHttp

        # Make authenticated request
        response = main.app.get_response('/auth/oauth2callback?code=dummy_code')
        headers  = {'Cookie': response.headers['Set-Cookie']}
        response = main.app.get_response('/dashboard', headers=headers)

        self.assertEqual(response.status_int, 200)