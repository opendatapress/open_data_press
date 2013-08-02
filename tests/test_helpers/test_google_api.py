# -*- coding: utf-8 -*-
import os
import unittest
from helpers import google_api
from oauth2client.client import OAuth2WebServerFlow


class GoogleAPITest(unittest.TestCase):

    def test_oauth2_flow(self):
        flow = google_api.oauth2_flow()
        self.assertIsInstance(flow, OAuth2WebServerFlow)

    def test_http_from_oauth2(self):
        self.assertIn('http_from_oauth2', dir(google_api))

    def test_user_info(self):
        self.assertIn('user_info', dir(google_api))
