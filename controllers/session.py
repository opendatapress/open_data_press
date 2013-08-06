# -*- coding: utf-8 -*-
#
# Session route handlers
#
import logging
from webapp2 import RequestHandler
from helpers import google_api
from helpers.sessions import SessionHandler
from oauth2client.client import FlowExchangeError
from oauth2client.anyjson import simplejson as json


# Build oAuth2 request and redirect to Google authentication endpoint
class LoginRoute(RequestHandler):
    def get(self):
        flow = google_api.oauth2_flow()
        self.redirect(flow.step1_get_authorize_url())


# Clear user session and return to home page
class LogoutRoute(SessionHandler):
    def get(self):
        if 'credentials' in self.session:
            del self.session['credentials']
        self.response.write('loged out')


# Show contents of session
class SessionRoute(SessionHandler):
    def get(self):
        self.response.write("<code>%s</code>" % self.session)


# Handle oAuth2 callback
# Create session and (if required) user account
class OAuth2CallbackRoute(SessionHandler):
    def get(self):
        
        code = self.request.GET.get('code')
        if None == code:
            return self.response.write('No authentication code returned')

        try:
            flow = google_api.oauth2_flow()
            auth = flow.step2_exchange(code).to_json()
            
            # TODO Create/update user record in DB
            # TODO Store credentials in DB rather than session
            # TODO Create session
            self.credentials(auth)
            
            # Get user info
            user_info = google_api.user_info(auth)

            # Show results
            body = '<a href="/auth/login">re-login</a><hr><code>%s</code><hr><code>%s</code>'
            self.response.write(body % (auth, json.dumps(user_info)))

        except FlowExchangeError as e:
            logging.error("oAuth2 Flow Exchange Error: %s" % e)
            self.response.write('Flow exchange error: %s' % e)
            
        except Exception as e:
            logging.error("oAuth2 Unknown Error: %s" % e)
            self.response.write('Something went wrong: %s' % e)