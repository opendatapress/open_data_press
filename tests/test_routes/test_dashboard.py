# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestDashboardHandler(unittest.TestCase):

    def test_main_path_responds(self):
        response = main.app.get_response('/dashboard')
        self.assertEqual(response.status_int, 200)