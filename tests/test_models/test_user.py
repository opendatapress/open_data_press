# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import testbed
from models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()


    def tearDown(self):
        self.testbed.deactivate()


    def test_user_properties_exist(self):
        self.user = User()
        self.assertTrue('created_at'          in dir(self.user))
        self.assertTrue('credentials'         in dir(self.user))
        self.assertTrue('google_birthday'     in dir(self.user))
        self.assertTrue('google_email'        in dir(self.user))
        self.assertTrue('google_gender'       in dir(self.user))
        self.assertTrue('google_id'           in dir(self.user))
        self.assertTrue('google_locale'       in dir(self.user))
        self.assertTrue('google_name'         in dir(self.user))
        self.assertTrue('google_picture_url'  in dir(self.user))
        self.assertTrue('modified_at'         in dir(self.user))
        self.assertTrue('profile_email'       in dir(self.user))
        self.assertTrue('profile_description' in dir(self.user))
        self.assertTrue('profile_name'        in dir(self.user))
        self.assertTrue('profile_slug'        in dir(self.user))
        self.assertTrue('profile_web_address' in dir(self.user))


    def test_user_class_methods_exist(self):
        self.assertTrue('get_by_slug' in dir(User))
        self.assertTrue('get_by_google_id' in dir(User))


    def test_get_by_slug(self):
        user_a = User(profile_slug = 'slug-1')
        user_a.put()
        user_b = User.get_by_slug('slug-1')
        self.assertEqual(user_a.key(), user_b.key())


    def test_get_by_google_id(self):
        user_a = User(google_id = '31459')
        user_a.put()
        user_b = User.get_by_google_id('31459')
        self.assertEqual(user_a.key(), user_b.key())


    def test_user_create_success(self):

        user_data = {}
        user_data['created_at']          = datetime.now()
        user_data['credentials']         = '{"token":"XXX"}'
        user_data['google_birthday']     = u'0000-01-01'
        user_data['google_email']        = u'test.user@gmail.com'
        user_data['google_gender']       = u'male'
        user_data['google_id']           = u'123456789'
        user_data['google_locale']       = u'en-GB'
        user_data['google_name']         = u'Test User'
        user_data['google_picture_url']  = u'https://lh3.googleusercontent.com/image.png'
        user_data['modified_at']         = datetime.now()
        user_data['profile_email']       = u'test.user@email.com'
        user_data['profile_description'] = u'This is a test user account'
        user_data['profile_name']        = u'Test User'
        user_data['profile_slug']        = 'test-user'
        user_data['profile_web_address'] = 'http://test-user.com'

        num_users = User.all().count()

        user_a = User()
        user_a.created_at          = user_data['created_at']
        user_a.credentials         = user_data['credentials']
        user_a.google_birthday     = user_data['google_birthday']
        user_a.google_email        = user_data['google_email']
        user_a.google_gender       = user_data['google_gender']
        user_a.google_id           = user_data['google_id']
        user_a.google_locale       = user_data['google_locale']
        user_a.google_name         = user_data['google_name']
        user_a.google_picture_url  = user_data['google_picture_url']
        user_a.modified_at         = user_data['modified_at']
        user_a.profile_email       = user_data['profile_email']
        user_a.profile_description = user_data['profile_description']
        user_a.profile_name        = user_data['profile_name']
        user_a.profile_slug        = user_data['profile_slug']
        user_a.profile_web_address = user_data['profile_web_address']
        user_a.put()

        self.assertEqual(num_users + 1, User.all().count())

        user_b = User.get(user_a.key())
        self.assertEqual(user_b.created_at,          user_data['created_at'])
        self.assertEqual(user_b.credentials,         user_data['credentials'])
        self.assertEqual(user_b.google_birthday,     user_data['google_birthday'])
        self.assertEqual(user_b.google_email,        user_data['google_email'])
        self.assertEqual(user_b.google_gender,       user_data['google_gender'])
        self.assertEqual(user_b.google_id,           user_data['google_id'])
        self.assertEqual(user_b.google_locale,       user_data['google_locale'])
        self.assertEqual(user_b.google_name,         user_data['google_name'])
        self.assertEqual(user_b.google_picture_url,  user_data['google_picture_url'])
        self.assertEqual(user_b.modified_at,         user_data['modified_at'])
        self.assertEqual(user_b.profile_email,       user_data['profile_email'])
        self.assertEqual(user_b.profile_description, user_data['profile_description'])
        self.assertEqual(user_b.profile_name,        user_data['profile_name'])
        self.assertEqual(user_b.profile_slug,        user_data['profile_slug'])
        self.assertEqual(user_b.profile_web_address, user_data['profile_web_address'])