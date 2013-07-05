# -*- coding: utf-8 -*-
#
# A data source
#

from google.appengine.ext import db

class DataSource(db.Model):

    # Properties
    google_spreadsheet = db.StringProperty()
    google_worksheet   = db.StringProperty()
    slug               = db.StringProperty()
    title              = db.StringProperty()
    description        = db.StringProperty()
    licence            = db.StringProperty()
    tags               = db.StringProperty()
    tbl_stars          = db.StringProperty()

