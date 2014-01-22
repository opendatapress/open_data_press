# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
import time
from webapp2 import RequestHandler
from helpers.views import render
from models.user import User
from models.data_source import DataSource

class HomeRoute(RequestHandler):
    def get(self):
        self.response.write(render('admin/layout.html'))


class ManageUsersRoute(RequestHandler):

    def get(self, user_id=None):
        if user_id:
            user = User.get_by_id(int(user_id))

            if not user:
                return self.response.write("No User with ID %s" % user_id)

            if 'delete' in self.request.GET:
                user.delete()
                return self.redirect('/admin/manage_users/')

            # Show user edit form
            data = {'user': user.to_dict()}
            return self.response.write(render('admin/manage_user_edit.html', data))

        # List all users
        users = [user.to_dict() for user in User.all().fetch(limit=None)]
        data = {'users': users}
        self.response.write(render('admin/manage_user_list.html', data))

    def post(self, user_id=None):
        if user_id:
            user = User.get_by_id(int(user_id))

            if user:
                user.profile_slug        = self.request.get('profile_slug')
                user.profile_name        = self.request.get('profile_name')
                user.profile_email       = self.request.get('profile_email')
                user.profile_web_address = self.request.get('profile_web_address')
                user.profile_description = self.request.get('profile_description')
                user.save()
                return self.redirect('/admin/manage_users/%s' % user.key().id())
                
        self.redirect('/admin/manage_users/')


class ManageDataSourcesRoute(RequestHandler):

    def get(self, data_source_id=None):
        if data_source_id:
            data_source = DataSource.get_by_id(int(data_source_id))

            if not data_source:
                return self.response.write("No Data Source with ID %s" % data_source_id)
                
            if 'delete' in self.request.GET:
                data_source.delete()
                return self.redirect('/admin/manage_data_sources/') 

            data = {'data_source': data_source.to_dict()}
            return self.response.write(render('admin/manage_data_source_edit.html', data))

        if 'user' in self.request.GET: 
            # List data sources for user
            user_id = int(self.request.get('user'))
            user = User.get_by_id(user_id)
            
            if not user:
                return self.response.write("No User with ID %s" % user_id)

            # List data sources belonging to user
            data_sources = [ds.to_dict() for ds in user.data_sources]

        else:
            # List all data sources
            data_sources = [ds.to_dict() for ds in DataSource.all().fetch(limit=None)]

        data = {'data_sources': data_sources}
        self.response.write(render('admin/manage_data_source_list.html', data))

    def post(self, data_source_id=None):
        if data_source_id:
            data_source = DataSource.get_by_id(int(data_source_id))

            if data_source:
                data_source.title       = self.request.get('title')
                data_source.slug        = self.request.get('slug')
                data_source.description = self.request.get('description')
                data_source.licence     = self.request.get('licence')
                data_source.tags        = self.request.get('tags')
                data_source.tbl_stars   = int(self.request.get('tbl_stars'))
                data_source.is_featured = bool(self.request.get('is_featured'))
                data_source.save()
                return self.redirect('/admin/manage_data_sources/%s' % data_source_id)

        self.redirect('/admin/manage_data_sources/')

class ManageDataViewsRoute(RequestHandler):
    def get(self):
        # List all data views
        # List all data views filtered by data source
        # Edit a data view
        # Delete a data view
        if self.request.get('action') and self.request.get('action') == 'edit':
            self.response.write(render('admin/manage_data_view_edit.html'))
        else:
            self.response.write(render('admin/manage_data_view_list.html'))


class ManageDatabaseRoute(RequestHandler):
    def get(self):
        # Resave all DB entires using current objetc model
        self.response.write(render('admin/manage_database.html'))


class ManageSearchRoute(RequestHandler):
    def get(self):
        # Empty search index and re-index all documents
        self.response.write(render('admin/manage_search.html'))


class BulkEmailRoute(RequestHandler):
    def get(self):
        # List of name <email> for all users
        self.response.write(render('admin/bulk_email.html'))

