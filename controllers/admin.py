# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
from webapp2 import RequestHandler
from helpers.views import render

class HomeRoute(RequestHandler):
    def get(self):
        self.response.write(render('admin/layout.html'))


class ManageUsersRoute(RequestHandler):
    def get(self):
        # List all users
        # Edit a user
        # Delete a user
        if self.request.get('action') and self.request.get('action') == 'edit':
            self.response.write(render('admin/manage_user_edit.html'))
        else:
            self.response.write(render('admin/manage_user_list.html'))


class ManageDataSourcesRoute(RequestHandler):
    def get(self):
        # List all data sources
        # List data sources filtered by user
        # Edit a data source
        # Delete a data source
        if self.request.get('action') and self.request.get('action') == 'edit':
            self.response.write(render('admin/manage_data_source_edit.html'))
        else:
            self.response.write(render('admin/manage_data_source_list.html'))


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

