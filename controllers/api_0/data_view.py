# -*- coding: utf-8 -*-
#
# API v0 data view route handlers
#
from datetime import datetime as DT
from oauth2client.anyjson import simplejson as json
from helpers.api_0_helpers import APIHandler, log_api_error
from models.user import User
from models.data_source import DataSource
from models.data_view import DataView


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
