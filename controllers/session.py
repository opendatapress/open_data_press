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
        if 'approval_prompt' in self.request.GET.keys():
            # Use /auth/login?approval_prompt to force refresh of authentication tokens
            flow = google_api.oauth2_flow(approval_prompt='force')
        else:
            flow = google_api.oauth2_flow()
        self.redirect(flow.step1_get_authorize_url())


# Clear user session and return to home page
class LogoutRoute(SessionHandler):
    def get(self):
        if 'credentials' in self.session:
            del self.session['credentials']
        self.redirect('/')


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
            # TODO Display cancelled login page

        try:
            flow = google_api.oauth2_flow()
            auth = flow.step2_exchange(code).to_json()
            
            # TODO Attempt to fetch user record from DB with matching google_id

            # TODO if not user exists with google id
                # TODO Create user record in DB

            # TODO if auth and user both have no refresh_token
                # TODO redirect to /auth/login?approval_prompt to get one
            
            # Get user info
            user_info = google_api.user_info(auth)
            # TODO Store updated user info in DB
            # TODO Store updated credentials in DB

            # Create session
            self.credentials(auth)

            # Show results
            body = 'Authenticated<br><a href="/auth/login">re-login</a> <a href="/auth/logout">logout</a><hr><code>%s</code><hr><code>%s</code>'
            self.response.write(body % (auth, json.dumps(user_info)))

            # TODO if any post-login redirects have been stored in the session
                # TODO delete redirect from session
                # TODO issue redirect

            # TODO redirect to dashboard

        except FlowExchangeError as e:
            logging.error("oAuth2 Flow Exchange Error: %s" % e)
            self.response.write('Flow exchange error: %s' % e)
            # TODO Display error reporting page
            
        except Exception as e:
            logging.error("oAuth2 Unknown Error: %s" % e)
            self.response.write('Something went wrong: %s' % e)
            # TODO Display error reporting page