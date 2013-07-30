# -*- coding: utf-8 -*-
#
# Dashboard route handlers
#

from webapp2 import RequestHandler

class MainRoute(RequestHandler):

    def get(self):
        self.response.write('')