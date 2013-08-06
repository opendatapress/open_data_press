# -*- coding: utf-8 -*-
#
# A mock class for httplib2 http client
#
# Inspired by: https://code.google.com/p/google-api-python-client/source/browse/tests/util.py

import os
import httplib2
import logging
from helpers import google_api


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_data(filename):
    f = file(os.path.join(DATA_DIR, filename), 'r')
    data = f.read()
    f.close()
    return data


class MockHttp(object):
    def request(self, uri, method="GET", body=None, headers=None, redirections=1, connection_type=None):

        # Response for oAuth2 Handshake
        if "https://accounts.google.com/o/oauth2/token" in uri:
            return httplib2.Response({'status': '200'}), load_data('oauth2_token.json')

        # Response for user info API
        if "https://www.googleapis.com/oauth2/v2/userinfo" in uri:
            return httplib2.Response({'status': '200'}), load_data('user_info.json')

        logging.error("No MockHTTP response for request to '%s'" % uri)
        return httplib2.Response({}), ''