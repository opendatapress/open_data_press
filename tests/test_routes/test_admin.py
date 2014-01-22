# -*- coding: utf-8 -*-

import unittest
import webapp2
import simplejson as json
import main # The app

from tests import dummy
from google.appengine.ext import testbed
from helpers import google_api
from models.user import User
from models.data_source import DataSource

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


    def create_data_source(self, user):
        ds = DataSource(**dummy.data_source)
        ds.user = user.key()
        ds.save()
        return ds


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


    def test_admin_manage_data_source_list(self):
        response = main.app.get_response('/admin/manage_data_sources')
        self.assertEqual(response.status_int, 200)

        
    def test_admin_manage_data_source_edit(self):
        user = self.create_user()
        data_source = self.create_data_source(user=user)
        data_source_id = data_source.key().id()

        response = main.app.get_response('/admin/manage_data_sources/%s' % data_source_id)
        self.assertEqual(response.status_int, 200)

        form_data = {
            'title':       'Test Data Source',
            'slug':        'test-data-source',
            'description': 'Test data source description',
            'licence':     'DWTFYL',
            'tags':        'alpha,beta,gamma',
            'tbl_stars':   '3',
            'is_featured': 'on'}

        response = main.app.get_response('/admin/manage_data_sources/%s' % data_source_id, POST=form_data)
        self.assertEqual(response.status_int, 302)
        self.assertTrue('/admin/manage_data_sources/%s' % data_source_id in response.location)

        data_source_b = DataSource.get_by_id(data_source_id)
        self.assertEqual(data_source_b.title,       form_data['title'])
        self.assertEqual(data_source_b.slug,        form_data['slug'])
        self.assertEqual(data_source_b.description, form_data['description'])
        self.assertEqual(data_source_b.licence,     form_data['licence'])
        self.assertEqual(data_source_b.tags,        form_data['tags'])
        self.assertEqual(data_source_b.tbl_stars,   int(form_data['tbl_stars']))
        self.assertEqual(data_source_b.is_featured, bool(form_data['is_featured']))


    def test_admin_manage_data_source_delete(self):
        user = self.create_user()
        data_source = self.create_data_source(user=user)
        data_source_id = data_source.key().id()

        response = main.app.get_response('/admin/manage_data_sources/%s/?delete' % data_source_id)
        self.assertEqual(response.status_int, 302)
        self.assertTrue('/admin/manage_data_sources/' in response.location)
        self.assertFalse(DataSource.get_by_id(data_source_id))
