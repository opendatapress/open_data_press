# -*- coding: utf-8 -*-
import os
import unittest
from helpers import google_api
from oauth2client.client import OAuth2WebServerFlow


class GoogleAPITest(unittest.TestCase):

    def test_oauth2_flow(self):
        flow = google_api.oauth2_flow()
        self.assertIsInstance(flow, OAuth2WebServerFlow)