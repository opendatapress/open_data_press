# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

from helpers.config import load_config, ConfigurationError
from oauth2client.client import OAuth2WebServerFlow

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