# -*- coding: utf-8 -*-
#
# A data view
#

from google.appengine.ext import db
from models.data_source import DataSource

class DataView(db.Model):

    # Properties
    template    = db.StringProperty(default=u'')
    mimetype    = db.StringProperty(default=u'')
    filetype    = db.StringProperty(default=u'')
    extension   = db.StringProperty(default=u'')
    data_source = db.ReferenceProperty(DataSource, collection_name="data_views")
