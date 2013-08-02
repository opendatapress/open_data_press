# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestSessionHandler(unittest.TestCase):

    def test_login_path_redirects_to_google_auth_endpoint(self):
        response = main.app.get_response('/auth/login')
        self.assertEqual(response.status_int, 302)
        self.assertIn('Location', response.headers)
        self.assertIn('accounts.google.com', response.headers['Location'])

    def test_logout_path_responds(self):
        response = main.app.get_response('/auth/logout')
        self.assertEqual(response.status_int, 200)

    def test_oauth2callback_path_responds(self):
        response = main.app.get_response('/auth/oauth2callback')
        self.assertEqual(response.status_int, 200)

    # TODO test oAuth2 authentication flow somehow...?