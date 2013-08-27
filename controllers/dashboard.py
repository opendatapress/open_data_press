# -*- coding: utf-8 -*-
#
# Dashboard route handlers
#

from helpers.sessions import SessionHandler
from helpers.views import render

class MainRoute(SessionHandler):

    def get(self):
        if self.current_user():
            data = {'session': self.session, 'current_user': self.current_user().to_dict()}
            body = render('dashboard.html', data)
            self.response.write(body)
        else:
            # Redirect if there is no authenticated user
            self.redirect('/auth/login')