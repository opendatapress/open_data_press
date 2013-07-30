# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler


class UserRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class DataSourceListRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class DataSourceItemRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def delete(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class DataViewListRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class DataViewItemRoute(RequestHandler):

    def get(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def delete(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class GoogleSheetsListRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class GoogleSheetsItemRoute(RequestHandler):

    def get(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class GoogleSheetsWorksheetRoute(RequestHandler):

    def get(self, google_sheets_id, worksheet_key):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')

    def post(self, google_sheets_id, worksheet_key):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success"}')


class Error404Route(RequestHandler):

    def get(self):
        self.response.set_status(404)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"error"}')