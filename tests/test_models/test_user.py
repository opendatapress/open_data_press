# -*- coding: utf-8 -*-

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from models.user import User
from tests import dummy


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()


    def tearDown(self):
        self.testbed.deactivate()


    def test_user_properties_exist(self):
        user = User(**dummy.user)
        self.assertTrue('created_at'          in dir(user))
        self.assertTrue('credentials'         in dir(user))
        self.assertTrue('google_birthday'     in dir(user))
        self.assertTrue('google_email'        in dir(user))
        self.assertTrue('google_gender'       in dir(user))
        self.assertTrue('google_id'           in dir(user))
        self.assertTrue('google_locale'       in dir(user))
        self.assertTrue('google_name'         in dir(user))
        self.assertTrue('google_picture_url'  in dir(user))
        self.assertTrue('last_login_at'       in dir(user))
        self.assertTrue('modified_at'         in dir(user))
        self.assertTrue('profile_email'       in dir(user))
        self.assertTrue('profile_description' in dir(user))
        self.assertTrue('profile_name'        in dir(user))
        self.assertTrue('profile_slug'        in dir(user))
        self.assertTrue('profile_web_address' in dir(user))
        self.assertTrue('data_sources'        in dir(user))


    def test_user_instance_methods_exist(self):
        user = User(**dummy.user)
        self.assertTrue('refresh_token' in dir(user))


    def test_user_class_methods_exist(self):
        self.assertTrue('get_by_slug' in dir(User))
        self.assertTrue('get_by_google_id' in dir(User))


    def test_get_by_slug(self):
        user = User(**dummy.user)
        user.put()
        self.assertEqual(user.key(), User.get_by_slug('test-user').key())


    def test_get_by_google_id(self):
        user = User(**dummy.user)
        user.put()
        self.assertEqual(user.key(), User.get_by_google_id('123456789').key())


    def test_user_create_success(self):
        num_users = User.all().count()
        user = User(**dummy.user)
        user.put()
        self.assertEqual(num_users + 1, User.all().count())

        user_b = User.get(user.key())
        self.assertEqual(user_b.created_at,          user.created_at)
        self.assertEqual(user_b.credentials,         user.credentials)
        self.assertEqual(user_b.google_birthday,     user.google_birthday)
        self.assertEqual(user_b.google_email,        user.google_email)
        self.assertEqual(user_b.google_gender,       user.google_gender)
        self.assertEqual(user_b.google_id,           user.google_id)
        self.assertEqual(user_b.google_locale,       user.google_locale)
        self.assertEqual(user_b.google_name,         user.google_name)
        self.assertEqual(user_b.google_picture_url,  user.google_picture_url)
        self.assertEqual(user_b.last_login_at,       user.last_login_at)
        self.assertEqual(user_b.modified_at,         user.modified_at)
        self.assertEqual(user_b.profile_email,       user.profile_email)
        self.assertEqual(user_b.profile_description, user.profile_description)
        self.assertEqual(user_b.profile_name,        user.profile_name)
        self.assertEqual(user_b.profile_slug,        user.profile_slug)
        self.assertEqual(user_b.profile_web_address, user.profile_web_address)


    def test_user_required_properties(self):

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.user.copy()
            del bad_params['created_at']
            User(**bad_params)
        self.assertTrue('created_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.user.copy()
            del bad_params['google_id']
            User(**bad_params)
        self.assertTrue('google_id' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.user.copy()
            del bad_params['last_login_at']
            User(**bad_params)
        self.assertTrue('last_login_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.user.copy()
            del bad_params['modified_at']
            User(**bad_params)
        self.assertTrue('modified_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.user.copy()
            del bad_params['profile_slug']
            User(**bad_params)
        self.assertTrue('profile_slug' in cm.exception.message)

