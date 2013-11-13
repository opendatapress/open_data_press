# -*- coding: utf-8 -*-
#
# A data view
#

from google.appengine.ext import db
from models.data_source import DataSource

class DataView(db.Model):

    # Properties
    created_at  = db.DateTimeProperty(required=True)
    data_source = db.ReferenceProperty(DataSource, collection_name="data_views")
    extension   = db.StringProperty(default=u'') # TODO restrict extension to approved list
    filetype    = db.StringProperty(default=u'') # TODO restrict filetype to approved list
    mimetype    = db.StringProperty(default=u'') # TODO restrict mimetype to approved list
    modified_at = db.DateTimeProperty(required=True)
    template    = db.TextProperty(default=u'')

    def to_dict(self):
        return {
            'created_at':  self.created_at.strftime('%Y-%m-%d %H:%M:%s'),
            'extension':   self.extension,
            'filetype':    self.filetype,
            'id':          self.key().id(),
            'mimetype':    self.mimetype,
            'modified_at': self.modified_at.strftime('%Y-%m-%d %H:%M:%s'),
            'template':    self.template,
        }

    def download_url(self):
        return "/%s/%s.%s" % (self.data_source.user.profile_slug, self.data_source.slug, self.extension)