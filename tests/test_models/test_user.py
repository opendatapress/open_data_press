# -*- coding: utf-8 -*-

import unittest
from models.user import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User()

    def test_user_google_id(self):
        self.assertTrue('google_id' in dir(self.user))

    def test_user_google_email(self):
        self.assertTrue('google_email' in dir(self.user))

    def test_user_google_name(self):
        self.assertTrue('google_name' in dir(self.user))

    def test_user_google_gender(self):
        self.assertTrue('google_gender' in dir(self.user))

    def test_user_google_locale(self):
        self.assertTrue('google_locale' in dir(self.user))

    def test_user_google_picture_url(self):
        self.assertTrue('google_picture_url' in dir(self.user))

    def test_user_google_birthday(self):
        self.assertTrue('google_birthday' in dir(self.user))

    def test_user_profile_slug(self):
        self.assertTrue('profile_slug' in dir(self.user))

    def test_user_profile_name(self):
        self.assertTrue('profile_name' in dir(self.user))

    def test_user_profile_email(self):
        self.assertTrue('profile_email' in dir(self.user))

    def test_user_profile_web_address(self):
        self.assertTrue('profile_web_address' in dir(self.user))

    def test_user_created_at(self):
        self.assertTrue('created_at' in dir(self.user))

    def test_user_modified_at(self):
        self.assertTrue('modified_at' in dir(self.user))

    def test_user_credentials(self):
        self.assertTrue('credentials' in dir(self.user))