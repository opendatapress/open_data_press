# -*- coding: utf-8 -*-
#
# Session route handlers
#
import logging
from webapp2 import RequestHandler
from helpers import google_api
from helpers.sessions import SessionHandler
from helpers.views import render
from controllers.root import error_500


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
            # TODO delete user_id from session
            del self.session['credentials']
        self.redirect('/')


# Handle oAuth2 callback
# Create session and (if required) user account
class OAuth2CallbackRoute(SessionHandler):
    def get(self):
        
        code = self.request.GET.get('code')
        if None == code:
            return self.response.write('No authentication code returned')
            # TODO Display cancelled login page
            self.redirect('/')

        try:
            flow = google_api.oauth2_flow()
            auth = flow.step2_exchange(code)
            
            # TODO Attempt to fetch user record from DB with matching google_id

            # TODO if not user exists with google id
                # TODO Create user record in DB

            # If we have no refresh token, redirect to /auth/login?approval_prompt to get one
            # TODO also check DB to prevent needless double-auth
            if None == auth.refresh_token:
                self.redirect('/auth/login?approval_prompt')

            # Get user info
            user_info = google_api.user_info(auth.to_json())
            # TODO Store updated user info in DB
            # TODO Store updated credentials in DB

            # Create session
            # TODO Store DB user_id in session
            self.credentials(auth.to_json())

            # TODO if any post-login redirects have been stored in the session
                # TODO delete redirect from session
                # TODO issue redirect

            # Show results
            # TODO redirect to dashboard instead
            data = {'message': 'Authenticated!', 'user_info': user_info, 'session': self.session}
            self.response.write(render('index.html', data))

        except Exception as e:
            error_500(self.request, self.response, e)