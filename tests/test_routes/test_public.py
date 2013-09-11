# -*- coding: utf-8 -*-

import unittest
import datetime
import webapp2
from google.appengine.ext import db
from google.appengine.ext import testbed
from models.user import User
import main # The app

class TestSessionHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        now = datetime.datetime.now()
        user = User(
            google_id     = u'1234567890', 
            profile_name  = u'Test User',
            profile_slug  = u'user-name', 
            created_at    = now, 
            modified_at   = now, 
            last_login_at = now)
        user.put()

    def tearDown(self):
        self.testbed.deactivate()

    def test_profile_path_responds(self):
        response = main.app.get_response('/user-name')
        self.assertEqual(response.status_int, 200)

    def test_data_source_path_responds(self):
        response = main.app.get_response('/user-name/data-1')
        self.assertEqual(response.status_int, 200)

    def test_data_view_path_responds(self):
        response = main.app.get_response('/user-name/data-1.ext')
        self.assertEqual(response.status_int, 200)

    def test_copy_data_source_path_responds(self):
        response = main.app.get_response('/user-name/data-1?copy')
        self.assertEqual(response.status_int, 200)