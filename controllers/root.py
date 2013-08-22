# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
import logging
from helpers.sessions import SessionHandler
from helpers.views import static, render

class HomeRoute(SessionHandler):

    def get(self):
        data = {'message': 'Hello World!', 'session': self.session}
        body = render('index.html', data)
        self.response.write(body)


def error_404(request, response, exception):
    msg_info = (request.method, request.path_url, request.POST.items(), exception)
    logging.error("%s %s %s 404 '%s'" % msg_info)
    response.write(static('404.html'))
    response.set_status(404)


def error_500(request, response, exception):
    msg_info = (request.method, request.path_url, request.POST.items(), exception)
    logging.error("%s %s %s 500 '%s'" % msg_info)
    response.write(static('500.html'))
    response.set_status(500)