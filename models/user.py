# -*- coding: utf-8 -*-
#
# A user class
#

from google.appengine.ext import db
from oauth2client.anyjson import simplejson as json

class User(db.Model):

    created_at          = db.DateTimeProperty(required=True)
    credentials         = db.TextProperty(default=u'')
    google_birthday     = db.StringProperty(default=u'')
    google_email        = db.EmailProperty()
    google_gender       = db.StringProperty(default=u'')
    google_id           = db.StringProperty(required=True)
    google_locale       = db.StringProperty(default=u'')
    google_name         = db.StringProperty(default=u'')
    google_picture_url  = db.StringProperty(default=u'')
    last_login_at       = db.DateTimeProperty(required=True)
    modified_at         = db.DateTimeProperty(required=True)
    profile_description = db.TextProperty(default=u'')
    profile_email       = db.TextProperty(default=u'')
    profile_name        = db.StringProperty(default=u'')
    profile_slug        = db.StringProperty(required=True)
    profile_web_address = db.TextProperty(default=u'')

    def refresh_token(self):
        if self.credentials:
            return json.loads(self.credentials).get('refresh_token')
        else:
            None

    def fetch_data_sources(self):
        return self.data_sources.order('-modified_at').fetch(limit=None)

    def to_dict(self):
        return {
            'created_at':          self.created_at.strftime('%Y-%m-%d %H:%M:%s'),
            'credentials':         self.credentials,
            'data_sources':        [ds.to_dict() for ds in self.fetch_data_sources()],
            'google_birthday':     self.google_birthday,
            'google_email':        self.google_email,
            'google_gender':       self.google_gender,
            'google_id':           self.google_id,
            'google_locale':       self.google_locale,
            'google_name':         self.google_name,
            'google_picture_url':  self.google_picture_url,
            'last_login_at':       self.last_login_at.strftime('%Y-%m-%d %H:%M:%s'),
            'modified_at':         self.modified_at.strftime('%Y-%m-%d %H:%M:%s'),
            'profile_description': self.profile_description,
            'profile_email':       self.profile_email,
            'profile_name':        self.profile_name,
            'profile_slug':        self.profile_slug,
            'profile_web_address': self.profile_web_address
            }

    @classmethod
    def get_by_slug(self, profile_slug):
        """ Find a user with the specified profile slug """
        return User.gql("WHERE profile_slug = :1", profile_slug).get()

    @classmethod
    def get_by_google_id(self, google_id):
        """ Find a user with the specified google id """
        return User.gql("WHERE google_id = :1", google_id).get()