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
        self.assertTrue('render'       in dir(dv))


    def test_data_view_required_properties(self):

        def create_data_view_with_missing_param(param):
            bad_params = dummy.data_view.copy()
            del bad_params[param]
            DataView(**bad_params)

        with self.assertRaisesRegexp(db.BadValueError, 'created_at') as cm:
            create_data_view_with_missing_param('created_at')

        with self.assertRaisesRegexp(db.BadValueError, 'modified_at') as cm:
            create_data_view_with_missing_param('modified_at')

        with self.assertRaisesRegexp(db.BadValueError, 'extension') as cm:
            create_data_view_with_missing_param('extension')

        with self.assertRaisesRegexp(db.BadValueError, 'mimetype') as cm:
            create_data_view_with_missing_param('mimetype')


    def test_data_view_required_values(self):

        def create_data_view_with_type(extension, mimetype):
            params = dummy.data_view.copy()
            params['extension'] = extension
            params['mimetype']  = mimetype
            dv = DataView(**params)
            dv.data_source = self.data_source.key()
            dv.put()
            return dv

        dv = create_data_view_with_type('txt', 'text/plain')
        self.assertTrue(dv.is_saved())

        dv = create_data_view_with_type('csv', 'text/csv')
        self.assertTrue(dv.is_saved())

        dv = create_data_view_with_type('xml', 'application/xml')
        self.assertTrue(dv.is_saved())

        dv = create_data_view_with_type('json', 'application/json')
        self.assertTrue(dv.is_saved())

        with self.assertRaisesRegexp(db.BadValueError, 'extension') as cm:
            create_data_view_with_type('bad_extension', 'text/plain')

        with self.assertRaisesRegexp(db.BadValueError, 'mimetype') as cm:
            create_data_view_with_type('txt', 'bad_mimetype')



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
        self.assertTrue('created_at'   in data)
        self.assertTrue('extension'    in data)
        self.assertTrue('filetype'     in data)
        self.assertTrue('id'           in data)
        self.assertTrue('mimetype'     in data)
        self.assertTrue('modified_at'  in data)
        self.assertTrue('source_id'    in data)
        self.assertTrue('template'     in data)
        self.assertTrue('download_url' in data)


    def test_data_view_method_download_url(self):
        dv  = self.make_data_view()
        url = "/%s/%s.%s" % (dv.data_source.user.profile_slug, dv.data_source.slug, dv.extension)
        self.assertEqual(url, dv.download_url())
