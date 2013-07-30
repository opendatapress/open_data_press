# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestDashboardHandler(unittest.TestCase):


    def test_api_path_responds(self):
        response = main.app.get_response('/api')
        self.assertEqual(response.status_int, 404)


    def test_api_0_path_responds(self):
        response = main.app.get_response('/api/0')
        self.assertEqual(response.status_int, 404)


    def test_api_0_user_path_responds(self):
        response = main.app.get_response('/api/0/user')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/user', method='POST')
        self.assertEqual(response.status_int, 200)


    def test_api_0_data_source_path_responds(self):
        response = main.app.get_response('/api/0/data_source')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source',method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1', method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1', method='DELETE')
        self.assertEqual(response.status_int, 200)


    def test_api_0_data_view_path_responds(self):
        response = main.app.get_response('/api/0/data_source/1/view')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1/view', method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1/view/0')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1/view/0', method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/data_source/1/view/0', method='DELETE')
        self.assertEqual(response.status_int, 200)


    def test_api_0_google_sheets_path_responds(self):
        response = main.app.get_response('/api/0/google/sheets')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/google/sheets', method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/google/sheets/0')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/google/sheets/0', method='POST')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/google/sheets/0/0')
        self.assertEqual(response.status_int, 200)

        response = main.app.get_response('/api/0/google/sheets/0/0', method='POST')
        self.assertEqual(response.status_int, 200)