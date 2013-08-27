# -*- coding: utf-8 -*-
#
# Session route handlers
#
import logging
from datetime import datetime
from webapp2 import RequestHandler
from helpers import google_api
from helpers.sessions import SessionHandler
from helpers.views import render
from controllers.root import error_500
from models.user import User

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
        if 'current_user' in self.session:
            del self.session['current_user']
        self.redirect('/')


# Handle oAuth2 callback
# Create session and (if required) user account
class OAuth2CallbackRoute(SessionHandler):
    def get(self):
        
        code = self.request.GET.get('code')
        if None == code:
            # TODO Display cancelled login page
            return self.response.write('No authentication code returned')

        try:
            flow      = google_api.oauth2_flow()
            auth      = flow.step2_exchange(code)
            now       = datetime.now()

            # Get Google user info
            google_user = google_api.user_info(auth.to_json())

            # Attempt to fetch user record from DB with matching google_id
            user = User.get_by_google_id(google_user.get('id'))

            # Create user if none exists
            if user == None:
                profile_slug = google_user['email'].split('@')[0]
                user = User(google_id=google_user.get('id'), profile_slug=profile_slug, created_at=now, modified_at=now, last_login_at=now)

            if user.refresh_token():
                # Do nothing if we have a refresh token
                pass
            elif None == user.refresh_token() and auth.refresh_token:
                # Store refresh token if we can
                user.credentials = auth.to_json()
            else:
                # Go get a refresh token if we need one
                return self.redirect('/auth/login?approval_prompt')

            # Update user account
            user.google_birthday    = google_user.get('birthday')
            user.google_email       = google_user.get('email')
            user.google_gender      = google_user.get('gender')
            user.google_locale      = google_user.get('locale')
            user.google_name        = google_user.get('name')
            user.google_picture_url = google_user.get('picture')
            user.last_login_at      = now
            user.put()

            # Create session
            self.current_user(user)

            # TODO if any post-login redirects have been stored in the session
                # TODO delete redirect from session
                # TODO issue redirect

            # TODO redirect to dashboard instead
            self.redirect('/dashboard')

        except Exception as e:
            logging.error(e)
            error_500(self.request, self.response, e)

        finally:
            pass