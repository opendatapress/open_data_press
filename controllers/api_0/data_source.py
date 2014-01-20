# -*- coding: utf-8 -*-
#
# API v0 data source route handlers
#
from datetime import datetime as DT
from oauth2client.anyjson import simplejson as json
from helpers import slug, search
from helpers.api_0_helpers import APIHandler, log_api_error
from models.user import User
from models.data_source import DataSource


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
            
            # Update Search Index
            search.index_doc(data_source.to_search_document())

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
            
            # Update Search Index
            search.index_doc(data_source.to_search_document())

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
            
            # Update Search Index
            search.delete_doc(str(data_source.key().id()))

            self.response.write('{"response":"success","body":"Data source deleted"}')

        except ValueError as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"%s"}' % e)
            self.response.set_status(404)

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem deleting data source"}')
            self.response.set_status(500)