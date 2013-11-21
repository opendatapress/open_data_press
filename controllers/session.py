# -*- coding: utf-8 -*-
#
# Session route handlers
#
import logging
from datetime import datetime
from helpers import google_api
from helpers.sessions import SessionHandler
from helpers.views import render
from helpers import slug
from controllers.root import error_500
from models.user import User

# Build oAuth2 request and redirect to Google authentication endpoint
class LoginRoute(SessionHandler):
    def get(self):

        # Store redirect URL if provided
        if 'redirect_url' in self.request.GET.keys():
            print self.request.GET['redirect_url']
            self.session['redirect_url'] = self.request.GET['redirect_url']
        
        # Force refresh of auth tokens for now issue#22
        flow = google_api.oauth2_flow(approval_prompt='force')

        # This is causing some problems I've not yet knocked all the kinks out of issue#22
        # if 'approval_prompt' in self.request.GET.keys():
        #     # Force refresh of authentication tokens
        #     flow = google_api.oauth2_flow(approval_prompt='force')
        # else:
        #     flow = google_api.oauth2_flow()

        url = flow.step1_get_authorize_url()
        logging.debug("Redirect to: %s" % url)
        self.redirect(url)


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

        logging.debug("Auth Code: %s" % code)
        logging.debug("Session (at start): %s" % self.session)

        if None == code:
            # TODO Display cancelled login page issue#27
            return self.response.write('No authentication code returned')

        try:
            flow = google_api.oauth2_flow()
            auth = flow.step2_exchange(code)
            now  = datetime.now()

            # Get Google user info
            google_user = google_api.user_info(auth.to_json())

            # Attempt to fetch user record from DB with matching google_id
            user = User.get_by_google_id(google_user.get('id'))

            # Create user if none exists
            if user == None:
                profile_slug = slug.create(google_user['email'].split('@')[0])
                user = User(
                    google_id     = google_user.get('id'), 
                    profile_name  = google_user.get('name'),
                    profile_slug  = profile_slug, 
                    created_at    = now, 
                    modified_at   = now, 
                    last_login_at = now)

            # TODO The following may be causing occasional invalid grant errors issue#22

            logging.debug("User Refresh Token: %s" % user.refresh_token())

            # Do nothing if we have a refresh token
            if user.refresh_token():
                logging.debug("User has existing Refresh Token")
                pass
        
            # Store refresh token if we can
            elif None == user.refresh_token() and auth.refresh_token:
                logging.debug("Storing Refresh Token for User")
                user.credentials = auth.to_json()
    
            # Go get a refresh token if we need one
            else:
                logging.debug("Fetching Refresh Token")
                logging.debug("Redirect to: /auth/login?approval_prompt")
                return self.redirect('/auth/login?approval_prompt')

            # Update user account
            # https://github.com/opendatapress/open_data_press/issues/5#issuecomment-23477495
            user.google_birthday    = google_user.get('birthday')
            user.google_email       = google_user.get('email')
            user.google_gender      = google_user.get('gender')
            user.google_locale      = google_user.get('locale')
            user.google_name        = google_user.get('name')
            user.google_picture_url = google_user.get('picture') # TODO or default if None issue#28
            user.last_login_at      = now
            user.put()

            # Create session
            logging.debug("Creating session for user: %s" % user.google_id)
            self.current_user(user)

            # Redirect to provided url if set
            if 'redirect_url' in self.session.keys():
                url = str(self.session['redirect_url'])
                del self.session['redirect_url']
                return self.redirect(url)

            # Redirect to dashboard instead
            logging.debug("Session (at end): %s" % self.session)
            logging.debug("Redirect to: /dashboard")
            self.redirect('/dashboard')

        except Exception as e:
            error_500(self.request, self.response, e)