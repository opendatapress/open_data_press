# -*- coding: utf-8 -*-

import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from models.user import User
from models.data_source import DataSource
from models.data_view import DataView
from tests import dummy


class TestDataViewModel(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.user = User(**dummy.user)
        self.user.put()
        self.data_source = DataSource(**dummy.data_source)
        self.data_source.user = self.user.key()
        self.data_source.put()


    def tearDown(self):
        self.testbed.deactivate()


    def make_data_view(self):
        dv = DataView(**dummy.data_view)
        dv.data_source = self.data_source.key()
        dv.put()
        return dv


    def test_data_view_properties_exist(self):
        dv = DataView(**dummy.data_view)
        self.assertTrue('created_at'  in dir(dv))
        self.assertTrue('extension'   in dir(dv))
        self.assertTrue('filetype'    in dir(dv))
        self.assertTrue('mimetype'    in dir(dv))
        self.assertTrue('modified_at' in dir(dv))
        self.assertTrue('template'    in dir(dv))


    def test_data_view_instance_methods_exist(self):
        dv = DataView(**dummy.data_view)
        self.assertTrue('to_dict'      in dir(dv))
        self.assertTrue('download_url' in dir(dv))


    def test_data_view_required_properties(self):
        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_view.copy()
            del bad_params['created_at']
            DataView(**bad_params)
        self.assertTrue('created_at' in cm.exception.message)

        with self.assertRaises(db.BadValueError) as cm:
            bad_params = dummy.data_view.copy()
            del bad_params['modified_at']
            DataView(**bad_params)
        self.assertTrue('modified_at' in cm.exception.message)


    def test_data_view_create(self):
        dv_count_a = DataView.all().count()
        dv = self.make_data_view()
        self.assertEqual(dv_count_a +1, DataView.all().count())


    def test_data_view_delete(self):
        dv = self.make_data_view()
        dv_count_a = DataView.all().count()
        dv.delete()
        self.assertEqual(dv_count_a -1, DataView.all().count())


    def test_data_view_method_to_dict(self):
        dv = self.make_data_view()
        data = dv.to_dict()
        self.assertTrue('created_at'  in data)
        self.assertTrue('extension'   in data)
        self.assertTrue('filetype'    in data)
        self.assertTrue('id'          in data)
        self.assertTrue('mimetype'    in data)
        self.assertTrue('modified_at' in data)
        self.assertTrue('template'    in data)