# -*- coding: utf-8 -*-
#
# A data source
#

from google.appengine.ext import db
from google.appengine.api import search
from models.user import User
from helpers import google_api

class DataSource(db.Model):

    # Properties
    created_at         = db.DateTimeProperty(required=True)
    description        = db.TextProperty(default=u'')
    google_spreadsheet = db.StringProperty(required=True)
    google_worksheet   = db.StringProperty(required=True)
    is_featured        = db.BooleanProperty(default=False)
    licence            = db.TextProperty(default=u'')
    modified_at        = db.DateTimeProperty(required=True)
    slug               = db.StringProperty(required=True)
    tags               = db.StringProperty(default=u'')
    tbl_stars          = db.IntegerProperty(default=0)
    title              = db.StringProperty(default=u'')
    user               = db.ReferenceProperty(User, collection_name="data_sources")

    def fetch_data_views(self):
        return self.data_views.order('-modified_at').fetch(limit=None)

    def to_dict(self):
        return {
            'created_at':         self.created_at.strftime('%Y-%m-%d %H:%M:%s'),
            'data_views':         [dv.to_dict() for dv in self.fetch_data_views()],
            'description':        self.description,
            'google_spreadsheet': self.google_spreadsheet,
            'google_worksheet':   self.google_worksheet,
            'id':                 self.key().id(),
            'is_featured':        self.is_featured,
            'licence':            self.licence,
            'modified_at':        self.modified_at.strftime('%Y-%m-%d %H:%M:%s'),
            'slug':               self.slug,
            'tags':               self.tags.split(','),
            'tbl_stars':          self.tbl_stars,
            'title':              self.title,
            'used_extensions':    self.used_extensions(),
            'user_id':            self.user.key().id(),
            'user_profile_name':  self.user.profile_name,
            'user_profile_slug':  self.user.profile_slug,
            'public_url':         self.public_url(),
            'spreadsheet_url':    self.spreadsheet_url(),
        }

    def to_search_document(self):
        """Returns a Google search document representation of the data source"""
        return search.Document(
            doc_id = str(self.key().id()),
            fields = [
                search.TextField(name='title',       value=self.title),
                search.TextField(name='description', value=self.description),
                search.TextField(name='tag',         value=self.tags),
                search.TextField(name='type',        value=" ".join(self.used_extensions())),
                search.NumberField(name='stars',     value=self.tbl_stars),
            ])

    def public_url(self):
        return "/%s/%s/" % (self.user.profile_slug, self.slug)

    def spreadsheet_url(self):
        return "https://docs.google.com/spreadsheet/ccc?key=%s" % self.google_spreadsheet

    def used_extensions(self):
        """A list of the extensions already in use by the data views of this data source"""
        return [dv.extension for dv in self.fetch_data_views()]

    def get_data(self, limit=None):
        """Fetch worksheet data from Google"""
        return google_api.get_cell_data(self.user.credentials, self.google_spreadsheet, self.google_worksheet, limit=limit)

    @classmethod
    def get_by_slug(self, user, slug):
        """ Find a data source, belonging to the user, with the specified profile slug """
        return user.data_sources.filter('slug =', slug).get()

    @classmethod
    def get_featured(self, limit=10):
        """Get data sources flagged as featured"""
        return DataSource.gql("WHERE is_featured = TRUE ORDER BY created_at DESC").fetch(limit=limit)