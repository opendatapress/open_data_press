# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
import main # The app

from tests import dummy
from google.appengine.ext import testbed
from helpers import google_api
from models.user import User

class TestAdminHandler(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def create_user(self):
        user = User(**dummy.user)
        user.save()
        return user

    def test_admin_manage_user_list(self):
        response = main.app.get_response('/admin/manage_users')
        self.assertEqual(response.status_int, 200)

    def test_admin_manage_user_edit(self):
        user = self.create_user()
        user_id = user.key().id()

        response = main.app.get_response('/admin/manage_users/%s' % user_id)
        self.assertEqual(response.status_int, 200)

        form_data = {
            'profile_slug':        'test-user',
            'profile_name':        'Test User',
            'profile_email':       'test@user.com',
            'profile_web_address': 'http://test-user.com',
            'profile_description': 'A Test User'}

        response = main.app.get_response('/admin/manage_users/%s' % user_id, POST=form_data)
        self.assertEqual(response.status_int, 302)
        self.assertTrue('/admin/manage_users/%s' % user_id in response.location)

        user_b = User.get_by_id(user_id)
        self.assertEqual(user_b.profile_slug,        form_data['profile_slug'])
        self.assertEqual(user_b.profile_name,        form_data['profile_name'])
        self.assertEqual(user_b.profile_email,       form_data['profile_email'])
        self.assertEqual(user_b.profile_web_address, form_data['profile_web_address'])
        self.assertEqual(user_b.profile_description, form_data['profile_description'])

    def test_admin_manage_user_delete(self):
        user = self.create_user()
        user_id = user.key().id()

        response = main.app.get_response('/admin/manage_users/%s?delete' % user_id)
        self.assertEqual(response.status_int, 302)
        self.assertTrue('/admin/manage_users/' in response.location)
        self.assertFalse(User.get_by_id(user_id))