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
        if 'https://accounts.google.com/o/oauth2/token' in uri:
            return httplib2.Response({'status': '200'}), load_data('oauth2_token.json')

        # Response for user info API
        if 'https://www.googleapis.com/oauth2/v2/userinfo' in uri:
            return httplib2.Response({'status': '200'}), load_data('user_info.json')

        # Response for Drive API discovery
        if 'https://www.googleapis.com/discovery/v1/apis/drive/v2/rest' in uri:
            return httplib2.Response({'status': '200'}), load_data('discovery_drive.json')

        # Response for files list
        if 'https://www.googleapis.com/drive/v2/files' in uri:
            return httplib2.Response({'status': '200'}), load_data('list_files.json')

        # Response for worksheets list
        if 'https://spreadsheets.google.com/feeds/worksheets/dummy_key/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheets.xml')

        # Response for worksheets list not found
        if 'https://spreadsheets.google.com/feeds/worksheets/not_found/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheets_not_found.xml')

        # Response for worksheets list with bad format
        if 'https://spreadsheets.google.com/feeds/worksheets/bad_format/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheets_bad_format.xml')

        # Response for worksheet cells
        if 'https://spreadsheets.google.com/feeds/list/dummy_key/dummy_id/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheet_cells.xml')

        # Response for worksheet cells not found
        if 'https://spreadsheets.google.com/feeds/list/dummy_key/not_found/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheet_cells_not_found.xml')

        # Response for worksheet cells with bad format
        if 'https://spreadsheets.google.com/feeds/list/dummy_key/bad_format/private/full' in uri:
            return httplib2.Response({'status': '200'}), load_data('worksheet_cells_bad_format.xml')

        logging.error("No MockHTTP response for request to '%s'" % uri)
        return httplib2.Response({}), ''