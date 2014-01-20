# -*- coding: utf-8 -*-
#
# Base routes and error handlers
#
import logging
from helpers import search
from helpers.sessions import SessionHandler
from helpers.views import static, render
from models.data_source import DataSource

class HomeRoute(SessionHandler):

    def get(self):
        data = {}
        data['current_user'] = self.current_user().to_dict() if self.current_user() else {}
        data['featured_data']  = [ds.to_dict() for ds in DataSource.get_featured(limit=5)]
        body = render('index.html', data)
        self.response.write(body)


class SearchRoute(SessionHandler):

    def get(self):
        # Search for published open data using Google Search API query language
        # https://developers.google.com/appengine/docs/python/search/query_strings
        current_user = self.current_user().to_dict() if self.current_user() else {}
        data = {'current_user': current_user, 'query': self.request.get('q'), 'num_results': 0, 'results': []}

        if data['query']:
            response = search.query(data['query'])
            data['results']     = [DataSource.get_by_id(int(r.doc_id)).to_dict() for r in response.results]
            data['num_results'] = response.number_found

        body = render('search.html', data)
        self.response.write(body)


def error_404(request, response, exception):
    msg_info = (request.method, request.path_url, request.POST.items(), exception)
    logging.error("%s %s %s 404 '%s'" % msg_info)
    response.write(render('404.html'))
    response.set_status(404)


def error_500(request, response, exception):
    msg_info = (request.method, request.path_url, request.POST.items(), exception, exception.__class__)
    logging.error("%s %s %s 500 '%s' %s" % msg_info)
    response.write(render('500.html'))
    response.set_status(500)