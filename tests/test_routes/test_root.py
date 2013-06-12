# -*- coding: utf-8 -*-

import unittest
import webapp2
import main # The app

class TestRootHandler(unittest.TestCase):

    def test_root_path_responds(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(main.app)
        self.assertEqual(response.status_int, 200)