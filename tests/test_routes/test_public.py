# -*- coding: utf-8 -*-

import unittest
import datetime
import webapp2
from google.appengine.ext import db
from google.appengine.ext import testbed
from models.user import User
from models.data_source import DataSource
from models.data_view import DataView
from tests import dummy
import main # The app

class TestSessionHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        now = datetime.datetime.now()
        user = User(**dummy.user)
        user.put()
        self.user = user

        ds = DataSource(**dummy.data_source)
        ds.user = user.key()
        ds.put()
        self.data_source = ds

        dv = DataView(**dummy.data_view)
        dv.data_source = ds.key()
        dv.put()
        self.data_view = dv

    def tearDown(self):
        self.testbed.deactivate()

    def test_profile_path_responds(self):
        url = "/%s" % self.user.profile_slug
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 200)

    def test_data_source_path_responds(self):
        url = "/%s/%s" % (self.user.profile_slug, self.data_source.slug)
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 200)

    def test_data_view_path_responds(self):
        url = "/%s/%s.%s" % (self.user.profile_slug, self.data_source.slug, self.data_view.extension)
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, self.data_view.mimetype)

    def test_copy_data_source_path_responds(self):
        response = main.app.get_response('/test-user/data-1?copy')
        self.assertEqual(response.status_int, 200)

    def test_broken_profile_path_fails(self):
        url = "/%s_bad" % self.user.profile_slug
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 404)

    def test_broken_data_source_path_fails(self):
        url = "/%s/%s_bad" % (self.user.profile_slug, self.data_source.slug)
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 404)

    def test_broken_data_view_path_fails(self):
        url = "/%s/%s.%s_bad" % (self.user.profile_slug, self.data_source.slug, self.data_view.extension)
        response = main.app.get_response(url)
        self.assertEqual(response.status_int, 404)
