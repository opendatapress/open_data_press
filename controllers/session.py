# -*- coding: utf-8 -*-
#
# Session route handlers
#
import logging
from webapp2 import RequestHandler
from helpers import google_api
from helpers.sessions import SessionHandler
from oauth2client.client import FlowExchangeError


# Build oAuth2 request and redirect to Google authentication endpoint
class LoginRoute(RequestHandler):
    def get(self):
        flow = google_api.oauth2_flow()
        self.redirect(flow.step1_get_authorize_url())


# Clear user session and return to home page
class LogoutRoute(RequestHandler):
    def get(self):
        self.response.write('logout')


# Handle oAuth2 callback
# Create session and (if required) user account
class OAuth2CallbackRoute(SessionHandler):
    def get(self):
        
        code = self.request.GET.get('code')
        if None == code:
            return self.response.write('No authentication code returned')

        try:
            flow = google_api.oauth2_flow()
            self.session['credentials'] = flow.step2_exchange(code).to_json()
            self.response.write('Authenticated <a href="/auth/login">re-login</a><br><code>%s</code>' % self.session['credentials'])
        except FlowExchangeError as e:
            logging.error("oAuth2 Flow Exchange Error: %s" % e)
            self.response.write('Flow exchange error: %s' % e)
        except Exception as e:
            logging.error("oAuth2 Unknown Error: %s" % e)
            self.response.write('Something went wrong: %s' % e)