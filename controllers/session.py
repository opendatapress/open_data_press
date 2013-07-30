# -*- coding: utf-8 -*-
#
# Session route handlers
#

from webapp2 import RequestHandler

class LoginRoute(RequestHandler):

    def get(self):
        self.response.write('')

class LogoutRoute(RequestHandler):

    def get(self):
        self.response.write('')

class OAuth2CallbackRoute(RequestHandler):

    def get(self):
        self.response.write('')