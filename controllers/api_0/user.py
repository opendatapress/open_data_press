# -*- coding: utf-8 -*-
#
# API v0 user route handlers
#
from datetime import datetime as DT
from oauth2client.anyjson import simplejson as json
from helpers.api_0_helpers import APIHandler, log_api_error
from models.user import User


class UserRoute(APIHandler):

    # Get the current user profile
    def get(self):
        try:
            # NB we have to decode "credentials" as it is stored as a string in the DB
            current_user = User.get_by_google_id(self.session['current_user']).to_dict()
            current_user["credentials"] = json.loads(current_user["credentials"])
            self.response.write('{"response":"success","body":%s}' % json.dumps(current_user, ensure_ascii=False))

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem fetching user profile"}')
            self.response.set_status(500)

    # Update the current user profile
    def post(self):
        try:
            data = json.loads(self.request.POST["payload"])
            user = User.get_by_google_id(self.session['current_user'])
            if None == user:
                self.response.write('{"response":"error","body":"Unknown User"}')
                self.response.set_status(500)
                return
            if "profile_name"        in data.keys(): user.profile_name        = data["profile_name"]
            if "profile_email"       in data.keys(): user.profile_email       = data["profile_email"]
            if "profile_description" in data.keys(): user.profile_description = data["profile_description"]
            if "profile_web_address" in data.keys(): user.profile_web_address = data["profile_web_address"]
            # TODO allow editing profile slug - must check for collisions - issue#46
            user.modified_at = DT.now()
            user.put()
            self.response.write('{"response":"success","body":%s}' % json.dumps(user.to_dict(), ensure_ascii=False))

        except Exception as e:
            log_api_error(self, e)
            self.response.write('{"response":"error","body":"Unknown problem updating profile"}')
            self.response.set_status(500)