# -*- coding: utf-8 -*-
#
# Helpers for working with views & static files
#
import jinja2
import os
import main
import logging
from datetime import datetime as dt

# Application renderer configured to load templates from the file system
APP_RENDER = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('./views')))


# Data renderer configured to use non-standard template tags
# https://github.com/opendatapress/open_data_press/issues/12
#
# <h1><%= title %></h1>
# <! This is a comment !>
# <% for row in data_rows %>
#     <p><%= row.code %> <%= row.title %></p>
# <% endfor %>
#
DATA_RENDER = jinja2.Environment('<%', '%>', '<%=', '%>', '<#', '#>', '~', '~~')

# Custom filters

# Attempt to read a string as datetime object
# If possible return a formatted date time string
def format_date_time(value, format='%Y-%m-%d %H:%M:%S'):
    try:
        return dt.strptime(value[0:19], "%Y-%m-%d %H:%M:%S").strftime(format)
    except Exception:
        return value

# Filters available in Application View Rendering
APP_RENDER.filters['datetime'] = format_date_time

# Filters availabel in Data View Rendering
DATA_RENDER.filters['datetime'] = format_date_time


# Render template using data
def render(template_file, template_data={}, ):
    template = APP_RENDER.get_template(template_file)
    template_data['VERSION'] = main.__version__
    return template.render(template_data)


# Read static file contents
def static(file_path):
    file_path = os.path.join(os.path.abspath('./static'), file_path)
    return open(file_path, 'r').read()


# Render a data template
# template : unicode string
# data : structrued data
def render_data(template, data={}):
    try:
        return DATA_RENDER.from_string(template).render(data)

    # TODO Consider allow execptions to surface to the request handler for issue#31

    except jinja2.exceptions.TemplateSyntaxError as e:
        logging.error("TEMPLATE\n%s" % template)
        logging.error("DATA\n%s" % data)
        logging.error("ERROR <%s> line %s, %s" % (e.__class__, e.lineno, e.message))
        return "Syntax error in template [line %s] %s" % (e.lineno, e.message)

    except jinja2.exceptions.TemplateError as e:
        logging.error("TEMPLATE\n%s" % template)
        logging.error("DATA\n%s" % data)
        logging.error("ERROR <%s> %s" % (e.__class__, e))
        return "Error in template - %s" % e

    except Exception as e:
        logging.error("TEMPLATE %s" % template)
        logging.error("DATA %s" % data)
        logging.error("ERROR <%s> %s" % (e.__class__, e))
        # Is this dangerous?
        return "Error in template - %s" % e