# -*- coding: utf-8 -*-
#
# Public site route handlers
#

from models.user import User
from models.data_source import DataSource
from helpers.views import render
from helpers.sessions import SessionHandler

class ProfileRoute(SessionHandler):

    def get(self, profile_slug):
        user = User.get_by_slug(profile_slug)
        # TODO get list of data sources
        if user:
            data = {'user': user.to_dict(), 'current_user': user.to_dict(), 'session': self.session}
            body = render('user_profile.html', data)
            self.response.write(body)
        else:
            # TODO 404
            self.response.write('No such user')


class DataSourceRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug):
        user = User.get_by_slug(profile_slug)
        data_source = DataSource.get_by_slug(data_source_slug)
        if user and data_source:
            if 'copy' in self.request.GET.keys():
                # TODO handler to duplicate data source in current_user profile
                self.response.write('copy data source')
            else:
                data = {'user': user.to_dict(), 'data_source': data_source.to_dict(), 'current_user': user.to_dict(), 'session': self.session}
                body = render('data_source.html', data)
                self.response.write(body)
        else:
            # TODO 404
            self.response.write('No such user or data source')


class DataViewRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug, data_view_ext):
        self.response.write('data view')