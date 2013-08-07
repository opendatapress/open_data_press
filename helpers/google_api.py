# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

import httplib2
from helpers.config import load_config, ConfigurationError
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client.anyjson import simplejson as json
from apiclient.discovery import build


# An oAuth2 authentication flow handler
def oauth2_flow():
    config = load_config()
    try:
        return OAuth2WebServerFlow(
            client_id     = config['google_api']['client_id'],
            client_secret = config['google_api']['client_secret'],
            scope         = " ".join(config['google_api']['scopes']),
            redirect_uri  = config['google_api']['redirect_uri'])
    except KeyError as e:
        raise ConfigurationError("Missing required configuration parameter %s" % e)


# Get an HTTP client authorised with oAuth2 credentials json
#
#  auth_json : a JSON object of valid credentials
#
def http_from_oauth2(auth_json):
    http  = httplib2.Http()
    creds = OAuth2Credentials.from_json(auth_json)
    return creds.authorize(http)


# Get user information using credentials json
#
#  auth_json : a JSON object of valid credentials
#
def user_info(auth_json):
    http = http_from_oauth2(auth_json)
    response = http.request('https://www.googleapis.com/oauth2/v2/userinfo')
    return json.loads(response[1])


# Set API client access to the drive API
def drive_service():
    return build('drive', 'v2')


# Get a list of files from Google Drive
# See: https://developers.google.com/drive/search-parameters
#
#  auth_json : a JSON object of valid credentials
#  query     : A search query string for the files API
#
def list_drive_files(auth_json, query=""):
    http = http_from_oauth2(auth_json)
    service = drive_service()
    file_list = []
    page_token = None
    while True:
        param = {'q': query}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute(http=http)
        file_list.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    return {'num_files': len(file_list), 'files':file_list}