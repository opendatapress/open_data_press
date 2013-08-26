# -*- coding: utf-8 -*-
#
# A user class
#

from google.appengine.ext import db
from oauth2client.anyjson import simplejson as json

class User(db.Model):

    created_at          = db.DateTimeProperty(required=True)
    credentials         = db.TextProperty()
    google_birthday     = db.StringProperty()
    google_email        = db.EmailProperty()
    google_gender       = db.StringProperty()
    google_id           = db.StringProperty(required=True)
    google_locale       = db.StringProperty()
    google_name         = db.StringProperty()
    google_picture_url  = db.LinkProperty()
    last_login_at       = db.DateTimeProperty(required=True)
    modified_at         = db.DateTimeProperty(required=True)
    profile_description = db.TextProperty()
    profile_email       = db.EmailProperty()
    profile_name        = db.StringProperty()
    profile_slug        = db.StringProperty(required=True)
    profile_web_address = db.LinkProperty()

    def refresh_token(self):
        if self.credentials:
            return json.loads(self.credentials).get('refresh_token')
        else:
            None

    @classmethod
    def get_by_slug(self, profile_slug):
        """ Find a user with the specified profile slug """
        return User.gql("WHERE profile_slug = :1", profile_slug).get()

    @classmethod
    def get_by_google_id(self, google_id):
        """ Find a user with the specified google id """
        return User.gql("WHERE google_id = :1", google_id).get()