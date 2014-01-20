# -*- coding: utf-8 -*-

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.api import search
from models.data_source import DataSource
from models.user import User
from tests import dummy


class TestDataSourceModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.user = User(**dummy.user)
        self.user.put()


    def tearDown(self):
        self.testbed.deactivate()


    def make_data_source(self):
        ds = DataSource(**dummy.data_source)
        ds.user = self.user.key()
        ds.put()
        return ds


    def test_data_source_properties_exist(self):
        ds = DataSource(**dummy.data_source)
        self.assertTrue('created_at'         in dir(ds))
        self.assertTrue('description'        in dir(ds))
        self.assertTrue('google_spreadsheet' in dir(ds))
        self.assertTrue('google_worksheet'   in dir(ds))
        self.assertTrue('licence'            in dir(ds))
        self.assertTrue('modified_at'        in dir(ds))
        self.assertTrue('slug'               in dir(ds))
        self.assertTrue('tags'               in dir(ds))
        self.assertTrue('tbl_stars'          in dir(ds))
        self.assertTrue('title'              in dir(ds))


    def test_data_source_instance_methods_exist(self):
        ds = DataSource(**dummy.data_source)
        self.assertTrue('to_dict' in dir(ds))
        self.assertTrue('to_search_document' in dir(ds))


    def test_data_source_required_properties(self):
        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_source.copy()
            del bad_params['created_at']
            DataSource(**bad_params)
        self.assertTrue('created_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_source.copy()
            del bad_params['modified_at']
            DataSource(**bad_params)
        self.assertTrue('modified_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_source.copy()
            del bad_params['slug']
            DataSource(**bad_params)
        self.assertTrue('slug' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_source.copy()
            del bad_params['google_worksheet']
            DataSource(**bad_params)
        self.assertTrue('google_worksheet' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_source.copy()
            del bad_params['google_spreadsheet']
            DataSource(**bad_params)
        self.assertTrue('google_spreadsheet' in cm.exception.message)


    def test_data_source_create(self):
        ds_count_a = DataSource.all().count()
        ds = self.make_data_source()
        self.assertEqual(ds_count_a + 1, DataSource.all().count())


    def test_data_source_delete(self):
        ds = self.make_data_source()
        ds_count_a = DataSource.all().count()
        ds.delete()
        self.assertEqual(ds_count_a -1, DataSource.all().count())


    def test_data_source_method_to_dict(self):
        ds = self.make_data_source()
        data = ds.to_dict()
        self.assertTrue('created_at'         in data)
        self.assertTrue('data_views'         in data)
        self.assertTrue('description'        in data)
        self.assertTrue('google_spreadsheet' in data)
        self.assertTrue('google_worksheet'   in data)
        self.assertTrue('id'                 in data)
        self.assertTrue('licence'            in data)
        self.assertTrue('modified_at'        in data)
        self.assertTrue('slug'               in data)
        self.assertTrue('tags'               in data)
        self.assertTrue('tbl_stars'          in data)
        self.assertTrue('title'              in data)
        self.assertTrue('user_id'            in data)

    def test_data_source_mnethod_to_search_document(self):
        ds = self.make_data_source()
        doc = ds.to_search_document()
        # Crude but functional
        self.assertEqual(doc.__class__, search.Document)
        self.assertEqual(len(doc.fields), 5)