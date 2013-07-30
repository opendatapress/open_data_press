# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestSessionHandler(unittest.TestCase):

    def test_login_path_responds(self):
        response = main.app.get_response('/auth/login')
        self.assertEqual(response.status_int, 200)

    def test_logout_path_responds(self):
        response = main.app.get_response('/auth/logout')
        self.assertEqual(response.status_int, 200)

    def test_oauth2callback_path_responds(self):
        response = main.app.get_response('/auth/oauth2callback')
        self.assertEqual(response.status_int, 200)