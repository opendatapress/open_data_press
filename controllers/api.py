# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler
from webapp2_extras.sessions import get_store
from oauth2client.client import OAuth2Credentials
from oauth2client.anyjson import simplejson as json

from helpers import google_api
from helpers.sessions import SessionHandler

import logging


#
# A request handler that denies any unauthenticated requests
#
class APIHandler(SessionHandler):
    def dispatch(self):
        # We have to get the session store directly as we only want to call the dispatch method 
        # of the parent class if the request is authenticated
        session = get_store(request=self.request).get_session()

        if 'credentials' in session.keys():
            self.response.content_type = 'application/json'
            SessionHandler.dispatch(self)
        else:
            self.response.content_type = 'application/json'
            self.response.write('{"response":"error","body":"Unauthenticated request"}')
            self.response.set_status(403)


class UserRoute(APIHandler):

    def get(self):
        self.response.write('{"response":"success","body":"user"}')

    def post(self):
        self.response.write('{"response":"success","body":"user"}')


class DataSourceListRoute(APIHandler):

    def get(self):
        self.response.write('{"response":"success","body":"data source list"}')

    def post(self):
        self.response.write('{"response":"success","body":"data source list"}')


class DataSourceItemRoute(APIHandler):

    def get(self, data_source_id):
        self.response.write('{"response":"success","body":"data source item"}')

    def post(self, data_source_id):
        self.response.write('{"response":"success","body":"data source item"}')

    def delete(self, data_source_id):
        self.response.write('{"response":"success","body":"data source item"}')


class DataViewListRoute(APIHandler):

    def get(self, data_source_id):
        self.response.write('{"response":"success","body":"data view list"}')

    def post(self, data_source_id):
        self.response.write('{"response":"success","body":"data view list"}')


class DataViewItemRoute(APIHandler):

    def get(self, data_source_id, data_view_id):
        self.response.write('{"response":"success","body":"data view item"}')

    def post(self, data_source_id, data_view_id):
        self.response.write('{"response":"success","body":"data view item"}')

    def delete(self, data_source_id, data_view_id):
        self.response.write('{"response":"success","body":"data view item"}')


class GoogleSheetsListRoute(APIHandler):

    def get(self):
        query = "trashed = false and hidden = false and mimeType = 'application/vnd.google-apps.spreadsheet'"
        drive_files = google_api.list_drive_files(self.credentials(), query=query)
        self.response.write('{"response":"success","body":%s}' % json.dumps(drive_files))

    def post(self):
        self.response.write('{"response":"success","body":"google sheets list"}')


class GoogleSheetsItemRoute(APIHandler):

    def get(self, google_sheets_id):
        sheet = google_api.get_worksheets(self.credentials(), google_sheets_id)
        if sheet['response'] == 'error':
            self.response.set_status(500)
            self.response.write(json.dumps(sheet))
        else:
            self.response.write(json.dumps(sheet))

    def post(self, google_sheets_id):
        self.response.write('{"response":"success","body":"google sheets item"}')


class GoogleSheetsWorksheetRoute(APIHandler):

    def get(self, google_sheets_id, worksheet_key):
        self.response.write('{"response":"success","body":"google sheets worksheet"}')

    def post(self, google_sheets_id, worksheet_key):
        self.response.write('{"response":"success","body":"google sheets worksheet"}')


class Error404Route(RequestHandler):

    def get(self):
        self.response.set_status(404)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"error","body":"Resource not found"}')