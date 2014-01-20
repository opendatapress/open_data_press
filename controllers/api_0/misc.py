# -*- coding: utf-8 -*-
#
# API v0 misc route handlers
#
from webapp2 import RequestHandler
from oauth2client.anyjson import simplejson as json
from helpers import google_api
from helpers.views import render_data
from helpers.api_0_helpers import APIHandler, log_api_error


class GoogleSheetsListRoute(APIHandler):

    # Get all Drive Spreadsheets accessible to the current user
    def get(self):
        try:
            page_token = self.request.GET["page_token"] if 'page_token' in self.request.GET.keys() else None
            query = "trashed = false and hidden = false and mimeType = 'application/vnd.google-apps.spreadsheet'"
            data  = google_api.list_drive_files(self.current_user().credentials, query=query, page_token=page_token)
            self.response.write('{"response":"success","body":%s}' % json.dumps(data, ensure_ascii=False))
        
        except google_api.GoogleAPIException as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(500)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem connecting to Google Drive"}')
            self.response.set_status(500)


class GoogleSheetsItemRoute(APIHandler):

    # Get info about a single spreadsheet (including all worksheets) accessible to the current user
    def get(self, google_sheets_id):
        try:
            data = google_api.get_worksheets(self.current_user().credentials, google_sheets_id)
            self.response.write('{"response":"success","body":%s}' % json.dumps(data, ensure_ascii=False))

        except google_api.GoogleAPIException as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(500)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem connecting to Google Drive"}')
            self.response.set_status(500)


class GoogleSheetsWorksheetRoute(APIHandler):

    # Get the data held in a single worksheet ina a single spreadsheet visible to the current user
    def get(self, google_sheets_id, worksheet_key):
        try:
            data = google_api.get_cell_data(self.current_user().credentials, google_sheets_id, worksheet_key)
            self.response.write('{"response":"success","body":%s}' % json.dumps(data, ensure_ascii=False))
        
        except google_api.GoogleAPIException as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(500)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem connecting to Google Drive"}')
            self.response.set_status(500)


class TemplatePreviewRoute(APIHandler):

    # Render a preview of the supplied template and data
    def post(self):
        try:
            payload = json.loads(self.request.POST["payload"])
            preview = render_data(payload['template'], payload['data'])
            data = {
                'data': payload['data'],
                'template': payload['template'],
                'preview': preview
            }
            self.response.write('{"response":"success","body":%s}' % json.dumps(data, ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"A probelm occured when generating the preview"}')
            self.response.set_status(500)


class Error404Route(RequestHandler):

    # 404 handler for API namespace
    def get(self):
        self.response.set_status(404)
        self.response.content_type = 'application/json'
        self.response.write('{"response":"error","body":"Resource not found"}')