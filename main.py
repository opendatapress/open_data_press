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
from controllers import api


__author__  = "YOUR NAME"
__website__ = "http://example.com"
__email__   = "you@example.com"
__licence__ = "MIT"
__version__ = "0.1"

# Map route patterns to controller handlers
routes = [

    # Home Root
    ('/',                                      root.HomeRoute),

    # Session
    (r'/auth/login/?',                         session.LoginRoute),
    (r'/auth/logout/?',                        session.LogoutRoute),
    (r'/auth/oauth2callback/?',                session.OAuth2CallbackRoute),

    # Dashboard
    (r'/dashboard/?',                          dashboard.MainRoute),

    # API
    (r'/api/0/google/sheets/?',                api.GoogleSheetsListRoute),
    (r'/api/0/google/sheets/(\w+)/?',          api.GoogleSheetsItemRoute),
    (r'/api/0/google/sheets/(\w+)/(\w+)/?',    api.GoogleSheetsWorksheetRoute),
    (r'/api/0/user/?',                         api.UserRoute),
    (r'/api/0/data_source/?',                  api.DataSourceListRoute),
    (r'/api/0/data_source/(\d+)/?',            api.DataSourceItemRoute),
    (r'/api/0/data_source/(\d+)/view/?',       api.DataViewListRoute),
    (r'/api/0/data_source/(\d+)/view/(\d+)/?', api.DataViewItemRoute),
    (r'/api/.*',                               api.Error404Route),
    (r'/api/?',                                api.Error404Route),

    # Public Site
    # Last in list for profile pattern matching
    (r'/([\w\-]+)/?',                          public.ProfileRoute),
    (r'/([\w\-]+)/([\w\-]+)/?',                public.DataSourceRoute),
    (r'/([\w\-]+)/([\w\-]+)\.([A-Za-z]+)?',    public.DataViewRoute),
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