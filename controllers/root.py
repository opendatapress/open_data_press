# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
import logging
from webapp2 import RequestHandler
from helpers.views import static, render

class HomeRoute(RequestHandler):

    def get(self):
        data = {'message': 'Hello World!'}
        body = render('index.html', data)
        self.response.write(body)


def error_404(request, response, exception):
    logging.error("%s - %s" % (request.path, exception))
    response.write(static('404.html'))
    response.set_status(404)


def error_500(request, response, exception):
    logging.error("%s - %s" % (request.path, exception))
    response.write(static('500.html'))
    response.set_status(500)