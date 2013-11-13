# -*- coding: utf-8 -*-

import unittest
from models.data_view import DataView
from tests import dummy


class TestDataViewModel(unittest.TestCase):

    def setUp(self):
        self.dv = DataView(**dummy.data_view)

    def test_data_view_template(self):
        self.assertTrue('template' in dir(self.dv))

    def test_data_view_mimetype(self):
        self.assertTrue('mimetype' in dir(self.dv))

    def test_data_view_filetype(self):
        self.assertTrue('filetype' in dir(self.dv))

    def test_data_view_extension(self):
        self.assertTrue('extension' in dir(self.dv))

