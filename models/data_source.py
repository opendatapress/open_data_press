# -*- coding: utf-8 -*-
#
# A data source
#

from google.appengine.ext import db
from models.user import User

class DataSource(db.Model):

    # Properties
    created_at         = db.DateTimeProperty(required=True)
    description        = db.StringProperty(default=u'')
    google_spreadsheet = db.StringProperty(required=True)
    google_worksheet   = db.StringProperty(required=True)
    licence            = db.StringProperty(default=u'')
    modified_at        = db.DateTimeProperty(required=True)
    slug               = db.StringProperty(required=True)
    tags               = db.StringProperty(default=u'')
    tbl_stars          = db.IntegerProperty(default=0)
    title              = db.StringProperty(default=u'')
    user               = db.ReferenceProperty(User, collection_name="data_sources")

    def to_dict(self):
        return {
            'created_at':         self.created_at.strftime('%Y-%M-%d %H:%m:%s'),
            'data_views':         [dv.to_dict() for dv in self.data_views.fetch(limit=None)],
            'description':        self.description,
            'google_spreadsheet': self.google_spreadsheet,
            'google_worksheet':   self.google_worksheet,
            'id':                 self.key().id(),
            'licence':            self.licence,
            'modified_at':        self.modified_at.strftime('%Y-%M-%d %H:%m:%s'),
            'slug':               self.slug,
            'tags':               self.tags.split(','),
            'tbl_stars':          self.tbl_stars,
            'title':              self.title,
            'public_url':         self.public_url(),
            'spreadsheet_url':    self.spreadsheet_url(),
        }

    def public_url(self):
        return "/%s/%s/" % (self.user.profile_slug, self.slug)

    def spreadsheet_url(self):
        return "https://docs.google.com/spreadsheet/ccc?key=%s" % self.google_spreadsheet

    def get_data(self):
        """ Fetch worksheet data from Google """
        # TODO
        return {}

    @classmethod
    def get_by_slug(self, slug):
        """ Find a user with the specified profile slug """
        return DataSource.gql("WHERE slug = :1", slug).get()