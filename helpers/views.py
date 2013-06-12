# -*- coding: utf-8 -*-
#
# Helpers for working with views & static files
#
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.abspath('./views')))

# Render template using data
def render(template_file, template_data={}, ):
    template = JINJA_ENVIRONMENT.get_template(template_file)
    return template.render(template_data)

# Read static file contents
def static(file_path):
    file_path = os.path.join(os.path.abspath('./static'), file_path)
    return open(file_path, 'r').read()