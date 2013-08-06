# -*- coding: utf-8 -*-
#
# Public site route handlers
#

from webapp2 import RequestHandler

class ProfileRoute(RequestHandler):

    def get(self, profile_slug):
        self.response.write('profile')

class DataSourceRoute(RequestHandler):

    def get(self, profile_slug, data_source_slug):
        if 'copy' in self.request.GET.keys():
            self.response.write('copy data source')
        else:
            self.response.write('view data source')

class DataViewRoute(RequestHandler):

    def get(self, profile_slug, data_source_slug, data_view_ext):
        self.response.write('data view')