# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#

from webapp2 import RequestHandler


class HomeRoute(RequestHandler):

    def get(self):
        body  = "Hello\nHere is your configuration\n"
        for item in self.app.config.items():
            body += " %s: %s\n" % item
        return self.response.write(body)


def error_404(request, response, exception):
    response.write("Error 404")
    response.set_status(404)


def error_500(request, response, exception):
    response.write("Error 500")
    response.set_status(500)