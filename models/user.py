# -*- coding: utf-8 -*-
#
# A user class
#

from google.appengine.ext import db

class User(db.Model):

    # Properties
    google_id           = db.StringProperty()
    google_email        = db.StringProperty()
    google_name         = db.StringProperty()
    profile_slug        = db.StringProperty()
    profile_name        = db.StringProperty()
    profile_email       = db.StringProperty()
    profile_web_address = db.StringProperty()
    created_at          = db.StringProperty()
    modified_at         = db.StringProperty()
    credentials         = db.StringProperty()