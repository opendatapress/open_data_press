# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler


class UserRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"user"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"user"}')


class DataSourceListRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source list"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source list"}')


class DataSourceItemRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')

    def delete(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')


class DataViewListRoute(RequestHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view list"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view list"}')


class DataViewItemRoute(RequestHandler):

    def get(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')

    def post(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')

    def delete(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')


class GoogleSheetsListRoute(RequestHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets list"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets list"}')


class GoogleSheetsItemRoute(RequestHandler):

    def get(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets item"}')

    def post(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets item"}')


class GoogleSheetsWorksheetRoute(RequestHandler):

    def get(self, google_sheets_id, worksheet_key):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets worksheet"}')

    def post(self, google_sheets_id, worksheet_key):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets worksheet"}')


class Error404Route(RequestHandler):

    def get(self):
        self.response.set_status(404)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"error","message":"Resource not found"}')