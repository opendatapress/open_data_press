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
from models.user import User

import logging


#
# A request handler that denies any unauthenticated requests
#
class APIHandler(SessionHandler):
    def dispatch(self):
        # We have to get the session store directly as we only want to call the dispatch method 
        # of the parent class if the request is authenticated
        session = get_store(request=self.request).get_session()

        if 'current_user' in session.keys():
            self.response.content_type = 'application/json'
            self.session = session
            SessionHandler.dispatch(self)
        else:
            self.response.content_type = 'application/json'
            self.response.write('{"response":"error","body":"Unauthenticated request"}')
            self.response.set_status(403)


class UserRoute(APIHandler):

    def get(self):
        # Return a json representation of the current user
        # NB we have to decode "credentials" as it is stored as a string in the DB
        current_user = User.get_by_google_id(self.session['current_user']).to_dict()
        current_user["credentials"] = json.loads(current_user["credentials"])
        self.response.write('{"response":"success","body":%s}' % json.dumps(current_user))

    def post(self):
        data = json.loads(self.request.POST["payload"])
        user = User.get_by_google_id(data["google_id"])
        if None == user:
            self.response.write('{"response":"error","body":"Unknown User"}')
            self.response.set_status(500)
            return
        try:
            if "profile_name"        in data.keys(): user.profile_name        = data["profile_name"]
            if "profile_email"       in data.keys(): user.profile_email       = data["profile_email"]
            if "profile_description" in data.keys(): user.profile_description = data["profile_description"]
            if "profile_web_address" in data.keys(): user.profile_web_address = data["profile_web_address"]
            user.put()
            self.response.write('{"response":"success","body":%s}' % json.dumps(user.to_dict()))
        except Exception as e:
            self.response.write('{"response":"error","body":"Problem updating profile"}')
            self.response.set_status(500)
            msg_info = (self.request.method, self.request.path_url, self.request.POST.items(), e, e.__class__)
            logging.error("%s %s %s 500 '%s' %s" % msg_info)


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
        try:
            query = "trashed = false and hidden = false and mimeType = 'application/vnd.google-apps.spreadsheet'"
            drive_files = google_api.list_drive_files(self.current_user().credentials, query=query)
            self.response.write(json.dumps(drive_files, ensure_ascii=False))
        except Exception as e:
            # TODO log error
            self.response.write('{"response":"error","body":"Problem connecting to Google Drive"}')
            self.response.set_status(500)


class GoogleSheetsItemRoute(APIHandler):

    def get(self, google_sheets_id):
        try:
            sheet = google_api.get_worksheets(self.current_user().credentials, google_sheets_id)
            if sheet['response'] == 'error':
                self.response.set_status(500)
            self.response.write(json.dumps(sheet, ensure_ascii=False))
        except Exception as e:
            # TODO log error
            self.response.write('{"response":"error","body":"Problem connecting to Google Drive"}')
            self.response.set_status(500)


class GoogleSheetsWorksheetRoute(APIHandler):

    def get(self, google_sheets_id, worksheet_key):
        try:
            data = google_api.get_cell_data(self.current_user().credentials, google_sheets_id, worksheet_key)
            if data['response'] == 'error':
                self.response.set_status(500)
            self.response.write(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            # TODO log error
            self.response.write('{"response":"error","body":"Problem connecting to Google Drive"}')
            self.response.set_status(500)


class Error404Route(RequestHandler):

    def get(self):
        self.response.set_status(404)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"error","body":"Resource not found"}')