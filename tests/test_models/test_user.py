# -*- coding: utf-8 -*-

import unittest
from models.user import User


class TestUserModel(unittest.TestCase):

    def test_user_name(self):
        user = User(name="Craig")
        self.assertEqual(user.name, "Craig")