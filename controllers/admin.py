# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
from helpers.sessions import SessionHandler
from helpers.views import render


class HomeRoute(SessionHandler):
    def get(self):

        html = """
        <h1>Admin Home</h1>
        <ul>
        <li><a href="/admin/manage_users">Manage Users</a></li>
        <li><a href="/admin/manage_data_views">Manage Data Views</a></li>
        <li><a href="/admin/manage_data_sources">Manage Data Sources</a></li>
        <li><a href="/admin/manage_database">Manage DataBase</a></li>
        <li><a href="/admin/manage_search">Manage Search</a></li>
        <li><a href="/admin/bulk_email">Bulk Email</a></li>
        </ul>
        """
        self.response.write(html)


class ManageUsersRoute(SessionHandler):
    def get(self):
        # List all users
        # Edit a user
        # Delete a user
        self.response.write("ManageUsersRoute")


class ManageDataSourcesRoute(SessionHandler):
    def get(self):
        # List all data sources
        # List data sources filtered by user
        # Edit a data source
        # Delete a data source
        self.response.write("ManageDataSourcesRoute")


class ManageDataViewsRoute(SessionHandler):
    def get(self):
        # List all data views
        # List all data views filtered by data source
        # Edit a data view
        # Delete a data view
        self.response.write("ManageDataViewsRoute")


class ManageDatabaseRoute(SessionHandler):
    def get(self):
        # Resave all DB entires using current objetc model
        self.response.write("ManageDatabaseRoute")


class ManageSearchRoute(SessionHandler):
    def get(self):
        # Empty search index and re-index all documents
        self.response.write("ManageSearchRoute")


class BulkEmailRoute(SessionHandler):
    def get(self):
        # List of name <email> for all users
        self.response.write("BulkEmailRoute")

