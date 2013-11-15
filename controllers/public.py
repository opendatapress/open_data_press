# -*- coding: utf-8 -*-
#
# Public site route handlers
#

from models.user import User
from models.data_source import DataSource
from models.data_view import DataView
from helpers.views import render
from helpers.sessions import SessionHandler
from controllers.root import error_404, error_500

class ProfileRoute(SessionHandler):

    def get(self, profile_slug):
        try:
            user = User.get_by_slug(profile_slug)
            if not user:
                raise ValueError("No user exists called %s" % profile_slug)

            current_user = self.current_user().to_dict() if self.current_user() else {}
            data = {'user': user.to_dict(), 'current_user': current_user}
            body = render('user_profile.html', data)
            self.response.write(body)

        except ValueError as e:
            error_404(self.request, self.response, e)

        except Exception as e:
            error_500(self.request, self.response, e)


class DataSourceRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug):
        try:
            user = User.get_by_slug(profile_slug)
            if not user:
                raise ValueError("No user exists called %s" % profile_slug)

            data_source = DataSource.get_by_slug(user, data_source_slug)
            if not data_source:
                raise ValueError("No data source exists with the slug %s" % data_source_slug)

            if 'copy' in self.request.GET.keys():
                # TODO handler to duplicate data source in current_user profile
                self.response.write('copy data source')
            else:
                current_user = self.current_user().to_dict() if self.current_user() else {}
                data = {'user': user.to_dict(), 'data_source': data_source.to_dict(), 'current_user': current_user}
                body = render('data_source.html', data)
                self.response.write(body)

        except ValueError as e:
            error_404(self.request, self.response, e)

        except Exception as e:
            error_500(self.request, self.response, e)


class DataViewRoute(SessionHandler):

    def get(self, profile_slug, data_source_slug, data_view_ext):
        try:
            user = User.get_by_slug(profile_slug)
            if not user:
                raise ValueError("No user exists called %s" % profile_slug)

            data_source = DataSource.get_by_slug(user, data_source_slug)
            if not data_source:
                raise ValueError("No data source exists with the slug %s" % data_source_slug)

            data_view = DataView.get_by_extension(data_source, data_view_ext)
            if not data_view:
                raise ValueError("No data view exists with the extension %s" % data_view_ext)

            self.response.content_type = str(data_view.mimetype)
            self.response.write(data_view.render())

        except ValueError as e:
            error_404(self.request, self.response, e)

        except Exception as e:
            error_500(self.request, self.response, e)