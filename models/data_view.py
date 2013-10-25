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

    def to_dict(self):
        return {
            'template': self.template,
            'mimetype': self.mimetype,
            'filetype': self.filetype,
            'extension': self.extension,
        }

    def download_url(self):
        return "/%s/%s.%s" % (self.data_source.user.profile_slug, self.data_source.slug, self.extension)