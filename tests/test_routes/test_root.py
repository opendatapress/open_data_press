# -*- coding: utf-8 -*-

import unittest
import webapp2
from google.appengine.ext import testbed
import main # The app

class TestRootHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_root_path_responds(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)