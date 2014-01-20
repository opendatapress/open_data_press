# -*- coding: utf-8 -*-
#
# The main application file
#

# Add 3rd-party library folder in to system path
import sys
sys.path.insert(0, 'lib')

from webapp2 import WSGIApplication
from helpers.config import load_config

# Explicitly import controller classes
from controllers import root
from controllers import public
from controllers import session
from controllers import dashboard
from controllers.api_0 import user        as api_user
from controllers.api_0 import data_source as api_data_source
from controllers.api_0 import data_view   as api_data_view
from controllers.api_0 import misc        as api_misc


__author__  = "Craig Russell"
__website__ = "http://opendatapress.org"
__email__   = "craig@craig-russell.co.uk"
__licence__ = "MIT"
__version__ = "0.1.0" # Display in view templates with {{VERSION}}

# Map route patterns to controller handlers
routes = [

    # Home Root
    ('/',                                       root.HomeRoute),

    # Session
    (r'/auth/login/?',                          session.LoginRoute),
    (r'/auth/logout/?',                         session.LogoutRoute),
    (r'/auth/oauth2callback/?',                 session.OAuth2CallbackRoute),

    # Dashboard
    (r'/dashboard/?',                           dashboard.MainRoute),

    # API
    (r'/api/0/user/?',                          api_user.UserRoute),
    (r'/api/0/data_source/?',                   api_data_source.DataSourceListRoute),
    (r'/api/0/data_source/(\d+)/?',             api_data_source.DataSourceItemRoute),
    (r'/api/0/data_source/(\d+)/view/?',        api_data_view.DataViewListRoute),
    (r'/api/0/data_source/(\d+)/view/(\d+)/?',  api_data_view.DataViewItemRoute),
    (r'/api/0/google/sheets/?',                 api_misc.GoogleSheetsListRoute),
    (r'/api/0/google/sheets/([\w\-]+)/?',       api_misc.GoogleSheetsItemRoute),
    (r'/api/0/google/sheets/([\w\-]+)/(\w+)/?', api_misc.GoogleSheetsWorksheetRoute),
    (r'/api/0/template/preview/?',              api_misc.TemplatePreviewRoute),
    (r'/api/.*',                                api_misc.Error404Route),
    (r'/api/?',                                 api_misc.Error404Route),

    # Public Site
    # Last in list for profile pattern matching
    (r'/([\w\-]+)/?',                           public.ProfileRoute),
    (r'/([\w\-]+)/([\w\-]+)/?',                 public.DataSourceRoute),
    (r'/([\w\-]+)/([\w\-]+)\.([A-Za-z]+)?',     public.DataViewRoute),
]


# Load config
config = load_config()


# Create the application
app = WSGIApplication(routes=routes, debug=config['debug'], config=config)


# Define error page handlers for production only
# We want to see full error traces during development
if not config['debug']:
    app.error_handlers[404] = root.error_404
    app.error_handlers[500] = root.error_500