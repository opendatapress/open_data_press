# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler
from oauth2client.client import OAuth2Credentials
from oauth2client.anyjson import simplejson as json

from helpers import google_api
from helpers.sessions import SessionHandler


class UserRoute(SessionHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"user"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"user"}')


class DataSourceListRoute(SessionHandler):

    def get(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source list"}')

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source list"}')


class DataSourceItemRoute(SessionHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')

    def delete(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data source item"}')


class DataViewListRoute(SessionHandler):

    def get(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view list"}')

    def post(self, data_source_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view list"}')


class DataViewItemRoute(SessionHandler):

    def get(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')

    def post(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')

    def delete(self, data_source_id, data_view_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"data view item"}')


class GoogleSheetsListRoute(SessionHandler):

    def get(self):
        credentials = self.session.get('credentials')
        query = "trashed = false and hidden = false and mimeType = 'application/vnd.google-apps.spreadsheet'"
        drive_files = google_api.list_drive_files(credentials, query=query)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":%s}' % json.dumps(drive_files))

    def post(self):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets list"}')


class GoogleSheetsItemRoute(SessionHandler):

    def get(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets item"}')

    def post(self, google_sheets_id):
        self.response.content_type = 'application/json'
        self.response.write('{"response":"success","body":"google sheets item"}')


class GoogleSheetsWorksheetRoute(SessionHandler):

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