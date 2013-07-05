# -*- coding: utf-8 -*-
#
# A data view
#

from google.appengine.ext import db

class DataView(db.Model):

    # Properties
    template  = db.StringProperty()
    mimetype  = db.StringProperty()
    filetype  = db.StringProperty()
    extension = db.StringProperty()
