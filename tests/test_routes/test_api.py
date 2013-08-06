# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
import main # The app

class TestAPIHandler(unittest.TestCase):

    # TODO test authenticated requests too

    def test_api_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api')
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)


    def test_api_0_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0')
        self.assertEqual(response.status_int, 404)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)


    def test_api_0_user_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/user')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')

        response = main.app.get_response('/api/0/user', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)


    def test_api_0_data_source_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/data_source')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source',method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1', method='DELETE')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)


    def test_api_0_data_view_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/data_source/1/view')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1/view', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1/view/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1/view/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/data_source/1/view/0', method='DELETE')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)


    def test_api_0_google_sheets_path_denies_unauthenticated_requests(self):
        response = main.app.get_response('/api/0/google/sheets')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/google/sheets', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/google/sheets/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/google/sheets/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/google/sheets/0/0')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)

        response = main.app.get_response('/api/0/google/sheets/0/0', method='POST')
        self.assertEqual(response.status_int, 403)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(json.loads(response.body), dict)