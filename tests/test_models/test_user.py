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


    def make_user(self):
        user = User(**dummy.user)
        user.put()
        return user


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
        self.assertTrue('to_dict' in dir(user))


    def test_user_class_methods_exist(self):
        self.assertTrue('get_by_slug' in dir(User))
        self.assertTrue('get_by_google_id' in dir(User))


    def test_user_create(self):
        num_users = User.all().count()
        user = self.make_user()
        self.assertEqual(num_users + 1, User.all().count())


    def test_user_delete(self):
        user = self.make_user()
        num_users = User.all().count()
        user.delete()
        self.assertEqual(num_users - 1, User.all().count())


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


    def test_user_method_get_by_slug(self):
        user = self.make_user()
        self.assertEqual(user.key(), User.get_by_slug(dummy.user['profile_slug']).key())


    def test_user_method_get_by_google_id(self):
        user = self.make_user()
        self.assertEqual(user.key(), User.get_by_google_id(dummy.user['google_id']).key())


    def test_user_method_to_dict(self):
        user = self.make_user()
        data = user.to_dict()
        self.assertTrue('created_at'          in data)
        self.assertTrue('credentials'         in data)
        self.assertTrue('google_birthday'     in data)
        self.assertTrue('google_email'        in data)
        self.assertTrue('google_gender'       in data)
        self.assertTrue('google_id'           in data)
        self.assertTrue('google_locale'       in data)
        self.assertTrue('google_name'         in data)
        self.assertTrue('google_picture_url'  in data)
        self.assertTrue('last_login_at'       in data)
        self.assertTrue('modified_at'         in data)
        self.assertTrue('profile_email'       in data)
        self.assertTrue('profile_description' in data)
        self.assertTrue('profile_name'        in data)
        self.assertTrue('profile_slug'        in data)
        self.assertTrue('profile_web_address' in data)
        self.assertTrue('data_sources'        in data)