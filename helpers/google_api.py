# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

import httplib2
from helpers.config import load_config, ConfigurationError
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client.anyjson import simplejson as json

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
def http_from_oauth2(auth_json):
    http  = httplib2.Http()
    creds = OAuth2Credentials.from_json(auth_json)
    return creds.authorize(http)

# Get user information using credentials json
def user_info(auth_json):
    http = http_from_oauth2(auth_json)
    response = http.request('https://www.googleapis.com/oauth2/v2/userinfo')
    return json.loads(response[1])