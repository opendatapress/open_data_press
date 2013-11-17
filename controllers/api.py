# -*- coding: utf-8 -*-
#
# Session route handlers
#
from datetime import datetime as DT

from webapp2 import RequestHandler
from webapp2_extras.sessions import get_store
from oauth2client.client import OAuth2Credentials
from oauth2client.anyjson import simplejson as json

from helpers import google_api, slug
from helpers.sessions import SessionHandler
from helpers.views import render_data
from models.user import User
from models.data_source import DataSource
from models.data_view import DataView

import logging


def log_api_error(obj,error):
    msg_info = (obj.request.method, obj.request.path_url, obj.request.POST.items(), error, error.__class__)
    logging.error("%s %s %s 500 '%s' %s" % msg_info)


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

    # Get the current user profile
    def get(self):
        try:
            # NB we have to decode "credentials" as it is stored as a string in the DB
            current_user = User.get_by_google_id(self.session['current_user']).to_dict()
            current_user["credentials"] = json.loads(current_user["credentials"])
            self.response.write('{"response":"success","body":%s}' % json.dumps(current_user, ensure_ascii=False))

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem fetching user profile"}')
            self.response.set_status(500)

    # Update the current user profile
    def post(self):
        try:
            data = json.loads(self.request.POST["payload"])
            user = User.get_by_google_id(self.session['current_user'])
            if None == user:
                self.response.write('{"response":"error","body":"Unknown User"}')
                self.response.set_status(500)
                return
            if "profile_name"        in data.keys(): user.profile_name        = data["profile_name"]
            if "profile_email"       in data.keys(): user.profile_email       = data["profile_email"]
            if "profile_description" in data.keys(): user.profile_description = data["profile_description"]
            if "profile_web_address" in data.keys(): user.profile_web_address = data["profile_web_address"]
            user.modified_at = DT.now()
            user.put()
            self.response.write('{"response":"success","body":%s}' % json.dumps(user.to_dict(), ensure_ascii=False))

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem updating profile"}')
            self.response.set_status(500)


class DataSourceListRoute(APIHandler):

    # Get all data sources owned by the current user
    def get(self):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_sources = current_user.fetch_data_sources()
            response = {
                'total_results': len(data_sources),
                'data_sources': [ds.to_dict() for ds in data_sources]
            }
            self.response.write('{"response":"success","body":%s}' % json.dumps(response, ensure_ascii=False))

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem fetching data sources"}')
            self.response.set_status(500)

    # Create a new data source for the current user
    def post(self):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            payload      = json.loads(self.request.POST["payload"])
            data_source  = DataSource(
                                google_spreadsheet = payload['key'],
                                google_worksheet   = payload['id'],
                                title              = payload['title'],
                                slug               = slug.create(payload['title']),
                                created_at         = DT.now(),
                                modified_at        = DT.now())
            data_source.user = current_user.key()
            data_source.put()
            self.response.write('{"response":"success","body":%s}' % json.dumps(data_source.to_dict(), ensure_ascii=False))

        except slug.SlugError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem creating slug for data source"}')
            self.response.set_status(500)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem creating data source"}')
            self.response.set_status(500)


class DataSourceItemRoute(APIHandler):

    # Get a single data source owned by the current user
    def get(self, data_source_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))
            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            self.response.write('{"response":"success","body":%s}' % json.dumps(data_source.to_dict(), ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem creating data source"}')
            self.response.set_status(500)

    # Update a single data source ownened by the current user
    def post(self, data_source_id):
        try:
            payload      = json.loads(self.request.POST["payload"])
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            if "description" in payload.keys(): data_source.description = payload['description']
            if "licence"     in payload.keys(): data_source.licence     = payload['licence']
            if "slug"        in payload.keys(): data_source.slug        = payload['slug']
            if "tags"        in payload.keys(): data_source.tags        = payload['tags']
            if "tbl_stars"   in payload.keys(): data_source.tbl_stars   = int(payload['tbl_stars'])
            if "title"       in payload.keys(): data_source.title       = payload['title']
            data_source.modified_at = DT.now()
            data_source.put()

            self.response.write('{"response":"success","body":%s}' % json.dumps(data_source.to_dict(), ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem updating data source"}')
            self.response.set_status(500)

    # Delete a single data source owned by the current user
    def delete(self, data_source_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            data_source.delete()
            self.response.write('{"response":"success","body":"Data source deleted"}')

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem deleting data source"}')
            self.response.set_status(500)


class DataViewListRoute(APIHandler):

    # List all data views of a single data source belonging to the current user
    def get(self, data_source_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            data_views = data_source.fetch_data_views()
            response = {
                'total_results': len(data_views),
                'data_views': [ds.to_dict() for ds in data_views]
            }
            self.response.write('{"response":"success","body":%s}' % json.dumps(response, ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem fetching data sources"}')
            self.response.set_status(500)

    # Create a new data view for a single data source belonging to the current user
    def post(self, data_source_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))
            payload    = json.loads(self.request.POST["payload"])

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            if payload['extension'] in data_source.used_extensions():
                raise ValueError("This Data Source already has a Data View of that type")

            data_view  = DataView(
                                extension   = payload['extension'],
                                mimetype    = payload['mimetype'],
                                created_at  = DT.now(),
                                modified_at = DT.now())
            if "filetype"  in payload.keys(): data_view.filetype = payload['filetype']
            data_view.data_source = data_source.key()
            data_view.put()
            self.response.write('{"response":"success","body":%s}' % json.dumps(data_view.to_dict(), ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem creating data source"}')
            self.response.set_status(500)


class DataViewItemRoute(APIHandler):

    # Get a data view for a single data source belonging to the current user
    def get(self, data_source_id, data_view_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))
            data_view    = DataView.get_by_id(int(data_view_id))

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            if data_view is None:
                raise ValueError("No Data View exists with id %s" % data_source_id)

            if not data_view.data_source.key() == data_source.key():
                raise ValueError("Data View with id %s does not belong to Data Source with id %s" % (data_view_id, data_source_id))

            self.response.write('{"response":"success","body":%s}' % json.dumps(data_view.to_dict(default_template=True), ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem fetching data source"}')
            self.response.set_status(500)

    # Update a data view of a single data source belonging to the current user
    def post(self, data_source_id, data_view_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))
            data_view    = DataView.get_by_id(int(data_view_id))
            payload      = json.loads(self.request.POST["payload"])

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            if data_view is None:
                raise ValueError("No Data View exists with id %s" % data_source_id)

            if not data_view.data_source.key() == data_source.key():
                raise ValueError("Data View with id %s does not belong to Data Source with id %s" % (data_view_id, data_source_id))

            if "template" in payload.keys(): 
                data_view.template = payload['template']
                data_view.modified_at = DT.now()
                data_view.put()

            self.response.write('{"response":"success","body":%s}' % json.dumps(data_view.to_dict(), ensure_ascii=False))

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem updating data source"}')
            self.response.set_status(500)

    # Delete a data view of a single data source belonging to the current user
    def delete(self, data_source_id, data_view_id):
        try:
            current_user = User.get_by_google_id(self.session['current_user'])
            data_source  = DataSource.get_by_id(int(data_source_id))
            data_view    = DataView.get_by_id(int(data_view_id))

            if data_source is None:
                raise ValueError("No Data Source exists with id %s" % data_source_id)

            if not data_source.user.key() == current_user.key():
                raise ValueError("Data Source with id %s does not belong to user '%s'" % (data_source_id, current_user.profile_slug))

            if data_view is None:
                raise ValueError("No Data View exists with id %s" % data_source_id)

            if not data_view.data_source.key() == data_source.key():
                raise ValueError("Data View with id %s does not belong to Data Source with id %s" % (data_view_id, data_source_id))

            data_view.delete()

            self.response.write('{"response":"success","body":"Data View deleted"}')

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem deleting data source"}')
            self.response.set_status(500)


class GoogleSheetsListRoute(APIHandler):

    # Get all Drive Spreadsheets accessible to the current user
    def get(self):
        try:
            query = "trashed = false and hidden = false and mimeType = 'application/vnd.google-apps.spreadsheet'"
            data  = google_api.list_drive_files(self.current_user().credentials, query=query)
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