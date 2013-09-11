# -*- coding: utf-8 -*-
#
# Public site route handlers
#

from models.user import User
from helpers.views import render
from helpers.sessions import SessionHandler

class ProfileRoute(SessionHandler):

    def get(self, profile_slug):
        user = User.get_by_slug(profile_slug)
        if user:
            data = {'user': user, 'current_user': user.to_dict(), 'session': self.session}
            body = render('user_profile.html', data)
            self.response.write(body)
        else:
            self.response.write('No such user')


class DataSourceRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug):
        if 'copy' in self.request.GET.keys():
            self.response.write('copy data source')
        else:
            self.response.write('view data source')

class DataViewRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug, data_view_ext):
        self.response.write('data view')