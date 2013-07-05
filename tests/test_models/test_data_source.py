# -*- coding: utf-8 -*-

import unittest
from models.data_source import DataSource


class TestDataSourceModel(unittest.TestCase):

    def setUp(self):
        self.ds = DataSource()

    def test_data_source_google_spreadsheet(self):
        self.assertTrue('google_spreadsheet' in dir(self.ds))

    def test_data_source_google_worksheet(self):
        self.assertTrue('google_worksheet' in dir(self.ds))

    def test_data_source_slug(self):
        self.assertTrue('slug' in dir(self.ds))

    def test_data_source_title(self):
        self.assertTrue('title' in dir(self.ds))

    def test_data_source_description(self):
        self.assertTrue('description' in dir(self.ds))

    def test_data_source_licence(self):
        self.assertTrue('licence' in dir(self.ds))

    def test_data_source_tags(self):
        self.assertTrue('tags' in dir(self.ds))

    def test_data_source_tbl_stars(self):
        self.assertTrue('tbl_stars' in dir(self.ds))
