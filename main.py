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


__author__  = "YOUR NAME"
__website__ = "http://example.com"
__email__   = "you@example.com"
__licence__ = "MIT"
__version__ = "0.1"


# Map route patterns to controller handlers
routes = [
    ('/', root.HomeRoute)
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