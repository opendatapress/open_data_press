# -*- coding: utf-8 -*-
#
# A data view
#
import logging
from google.appengine.ext import db
from models.data_source import DataSource
from helpers.views import render_data, render

class DataView(db.Model):

    # Valid file types
    valid_extensions = ['txt',        'csv',      'xml',             'json',             'html',     ]
    valid_mimetypes  = ['text/plain', 'text/csv', 'application/xml', 'application/json', 'text/html',]

    # Properties
    created_at  = db.DateTimeProperty(required=True)
    data_source = db.ReferenceProperty(DataSource, collection_name="data_views")
    extension   = db.StringProperty(choices=valid_extensions, required=True)
    filetype    = db.StringProperty(default=u'')
    mimetype    = db.StringProperty(choices=valid_mimetypes, required=True)
    modified_at = db.DateTimeProperty(required=True)
    template    = db.TextProperty(default=u'')

    def to_dict(self, default_template=False):
        data = {
            'created_at':   self.created_at.strftime('%Y-%m-%d %H:%M:%s'),
            'download_url': self.download_url(),
            'extension':    self.extension,
            'filetype':     self.filetype,
            'id':           self.key().id(),
            'mimetype':     self.mimetype,
            'modified_at':  self.modified_at.strftime('%Y-%m-%d %H:%M:%s'),
            'source_id':    self.data_source.key().id(),
            'template':     self.template,
        }

        if default_template:
            data['data_preview']     = self.data_source.get_data(limit=5)
            data['default_template'] = self.default_template(data['data_preview'])
            # Use the default template, if one is not already set
            if not data['template']:
                data['template'] = data['default_template'] 

        return data

    def download_url(self):
        return "/%s/%s.%s" % (self.data_source.user.profile_slug, self.data_source.slug, self.extension)

    def render(self, limit=None):
        data     = self.data_source.get_data(limit=limit)
        template = self.template
        return render_data(template, data)

    def default_template(self, source_data):
        """Return a generated default template for this view type"""
        try: 
            return render('default_template.%s' % self.extension, source_data)

        except Exception as e:
            logging.error("ERROR %s, %s" % (e.__class__, e))
            return u"Sorry, I couldn't generate a default template for %s" % self.filetype

    @classmethod
    def get_by_extension(self, data_source, extension):
        """ Find a data view with the specified extension """
        return data_source.data_views.filter('extension =', extension).get()