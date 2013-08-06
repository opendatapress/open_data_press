# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestSessionHandler(unittest.TestCase):

    def test_profile_path_responds(self):
        response = main.app.get_response('/user-name')
        self.assertEqual(response.status_int, 200)

    def test_data_source_path_responds(self):
        response = main.app.get_response('/user-name/data-1')
        self.assertEqual(response.status_int, 200)

    def test_data_view_path_responds(self):
        response = main.app.get_response('/user-name/data.ext')
        self.assertEqual(response.status_int, 200)

    def test_copy_data_source_path_responds(self):
        response = main.app.get_response('/user-name/data-1?copy')
        self.assertEqual(response.status_int, 200)