# -*- coding: utf-8 -*-
#
# A data view
#

from google.appengine.ext import db
from models.data_source import DataSource

class DataView(db.Model):

    # Properties
    template    = db.StringProperty()
    mimetype    = db.StringProperty()
    filetype    = db.StringProperty()
    extension   = db.StringProperty()
    data_source = db.ReferenceProperty(DataSource, collection_name="data_views")
