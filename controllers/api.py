# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler


class UserRoute(RequestHandler):

    def get(self):
        self.response.write('')

    def post(self):
        self.response.write('')


class DataSourceListRoute(RequestHandler):

    def get(self):
        self.response.write('')

    def post(self):
        self.response.write('')


class DataSourceItemRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.write('')

    def post(self, data_source_id):
        self.response.write('')

    def delete(self, data_source_id):
        self.response.write('')


class DataViewListRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.write('')

    def post(self, data_source_id):
        self.response.write('')


class DataViewItemRoute(RequestHandler):

    def get(self, data_source_id, data_view_id):
        self.response.write('')

    def post(self, data_source_id, data_view_id):
        self.response.write('')

    def delete(self, data_source_id, data_view_id):
        self.response.write('')


class GoogleSheetsListRoute(RequestHandler):

    def get(self):
        self.response.write('')

    def post(self):
        self.response.write('')


class GoogleSheetsItemRoute(RequestHandler):

    def get(self, google_sheets_id):
        self.response.write('')

    def post(self, google_sheets_id):
        self.response.write('')


class GoogleSheetsWorksheetRoute(RequestHandler):

    def get(self, google_sheets_id, worksheet_key):
        self.response.write('')

    def post(self, google_sheets_id, worksheet_key):
        self.response.write('')


class Error404Route(RequestHandler):

    def get(self):
        self.response.set_status(404)
        self.response.write('')