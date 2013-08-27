# -*- coding: utf-8 -*-

import unittest
import webapp2
from datetime import datetime
from tests.utils import MockHttp
from google.appengine.ext import db
from google.appengine.ext import testbed
from helpers import google_api
from models.user import User
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

    def test_oauth2callback_path_succeeds_for_new_user(self):
        google_api.httplib2.Http = MockHttp

        num_users = User.all().count()
        response = main.app.get_response('/auth/oauth2callback?code=abc123')

        # Ensure new user record has been created with info from Google (data/user_info.json)
        user = User.get_by_google_id('12345')
        self.assertEqual(num_users+1,             User.all().count())
        self.assertEqual(user.google_birthday,    '0000-01-01')
        self.assertEqual(user.google_email,       'dummy_user@gmail.com')
        self.assertEqual(user.google_gender,      'male')
        self.assertEqual(user.google_locale,      'en-GB')
        self.assertEqual(user.google_name,        'Dummy User')
        self.assertEqual(user.google_picture_url, 'https://lh3.googleusercontent.com/photo.jpg')

        # Ensure correct response
        self.assertEqual(response.status_int, 302)
        self.assertTrue('Location' in response.headers)
        self.assertTrue('http://localhost/' in response.headers['Location'])

    def test_oauth2callback_path_succeeds_for_existing_user(self):
        google_api.httplib2.Http = MockHttp

        # Create dummy user
        now  = datetime.now()
        user = User(profile_slug='dummy_user', google_id='12345', created_at=now, last_login_at=now, modified_at=now)
        user.put()
        num_users = User.all().count()

        response = main.app.get_response('/auth/oauth2callback?code=abc123')

        # Ensure existing user record has been updated with info from Google (data/user_info.json)
        user = User.get_by_google_id('12345')
        self.assertEqual(num_users,               User.all().count())
        self.assertEqual(user.google_birthday,    '0000-01-01')
        self.assertEqual(user.google_email,       'dummy_user@gmail.com')
        self.assertEqual(user.google_gender,      'male')
        self.assertEqual(user.google_locale,      'en-GB')
        self.assertEqual(user.google_name,        'Dummy User')
        self.assertEqual(user.google_picture_url, 'https://lh3.googleusercontent.com/photo.jpg')

        # Ensure correct response
        self.assertEqual(response.status_int, 302)
        self.assertTrue('Location' in response.headers)
        self.assertTrue('http://localhost/' in response.headers['Location'])