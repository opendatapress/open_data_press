# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler

class LoginRoute(RequestHandler):

    def get(self):
        self.response.write('login')

class LogoutRoute(RequestHandler):

    def get(self):
        self.response.write('logout')

class OAuth2CallbackRoute(RequestHandler):

    def get(self):
        self.response.write('oauth2callback')