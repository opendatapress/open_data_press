# -*- coding: utf-8 -*-

import unittest
from models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        """ Create a user object """
        self.user = User()

    def test_user_google_id(self):
        """ Test user object property 'google_id' """
        self.assertTrue('google_id' in dir(self.user))

    def test_user_google_email(self):
        """ Test user object property 'google_email' """
        self.assertTrue('google_email' in dir(self.user))

    def test_user_google_name(self):
        """ Test user object property 'google_name' """
        self.assertTrue('google_name' in dir(self.user))

    def test_user_profile_slug(self):
        """ Test user object property 'profile_slug' """
        self.assertTrue('profile_slug' in dir(self.user))

    def test_user_profile_name(self):
        """ Test user object property 'profile_name' """
        self.assertTrue('profile_name' in dir(self.user))

    def test_user_profile_email(self):
        """ Test user object property 'profile_email' """
        self.assertTrue('profile_email' in dir(self.user))

    def test_user_profile_web_address(self):
        """ Test user object property 'profile_web_address' """
        self.assertTrue('profile_web_address' in dir(self.user))

    def test_user_created_at(self):
        """ Test user object property 'created_at' """
        self.assertTrue('created_at' in dir(self.user))

    def test_user_modified_at(self):
        """ Test user object property 'modified_at' """
        self.assertTrue('modified_at' in dir(self.user))

    def test_user_credentials(self):
        """ Test user object property 'credentials' """
        self.assertTrue('credentials' in dir(self.user))