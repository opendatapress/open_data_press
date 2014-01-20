# -*- coding: utf-8 -*-
#
# Helpers for v0 of th application API
#
from webapp2_extras.sessions import get_store
from helpers.sessions import SessionHandler
from models.user import User
import logging

#
# Helper to log api errors nicely
#
def log_api_error(obj, error):
    current_user = User.get_by_google_id(obj.session['current_user'])
    msg_info = (obj.request.method, obj.request.path_url, obj.request.POST.items(), error, error.__class__, current_user.profile_slug)
    logging.error("%s %s %s 500 '%s' %s [%s]" % msg_info)


#
# A request handler that denies any unauthenticated requests
#
class APIHandler(SessionHandler):
    def dispatch(self):
        # We have to get the session store directly as we only want to call the dispatch method 
        # of the parent class if the request is authenticated
        session = get_store(request=self.request).get_session()

        if 'current_user' in session.keys():
            self.response.content_type = 'application/json'
            self.session = session
            SessionHandler.dispatch(self)
        else:
            self.response.content_type = 'application/json'
            self.response.write('{"response":"error","body":"Unauthenticated request"}')
            self.response.set_status(403)