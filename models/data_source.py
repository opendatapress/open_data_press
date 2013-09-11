# -*- coding: utf-8 -*-
#
# A data source
#

from google.appengine.ext import db
from models.user import User

class DataSource(db.Model):

    # Properties
    created_at         = db.DateTimeProperty(required=True)
    description        = db.StringProperty()
    google_spreadsheet = db.StringProperty(required=True)
    google_worksheet   = db.StringProperty(required=True)
    licence            = db.StringProperty()
    modified_at        = db.DateTimeProperty(required=True)
    slug               = db.StringProperty(required=True)
    tags               = db.StringProperty()
    tbl_stars          = db.StringProperty()
    title              = db.StringProperty()
    user               = db.ReferenceProperty(User, collection_name="data_sources")

