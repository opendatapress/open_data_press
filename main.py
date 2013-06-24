# -*- coding: utf-8 -*-
#
# The main application file
#

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


# Load config and set debug flag
debug, config = load_config()


# Create the application
app = WSGIApplication(routes=routes, debug=debug, config=config)


# Define error page handlers for production only
# We want to see full error traces during development
if not debug:
    app.error_handlers[404] = root.error_404
    app.error_handlers[500] = root.error_500