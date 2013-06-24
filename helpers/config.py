# -*- coding: utf-8 -*-
#
# A helper method to load configuration files
#

import os
import yaml


def load_config():
    """ Load configuration and set debug flag for this environment """
    
    # Load global configuration
    config = yaml.load(open(os.path.abspath('./conf/global.yaml'), 'r').read())

    # Detect development or production environment and configure accordingly
    if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
        conf_f = open(os.path.abspath('./conf/development.yaml'), 'r')
        config = dict(config.items() + yaml.load(conf_f.read()).items())
    else:
        conf_f = open(os.path.abspath('./conf/production.yaml'), 'r')
        config = dict(config.items() + yaml.load(conf_f.read()).items())

    return config