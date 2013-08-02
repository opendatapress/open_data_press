# -*- coding: utf-8 -*-
#
# Usage: runtests.py SDK_PATH TEST_PATH
# Run unit test for App Engine apps.
#
# SDK_PATH    Path to the SDK installation
# TEST_PATH   Path to package containing test modules
#
# Options:
#   -h, --help  show this help message and exit
#
# Adapted from:
# https://developers.google.com/appengine/docs/python/tools/localunittesting

import sys
sys.path.insert(0, 'lib')
import os
import unittest
import optparse


USAGE = """%prog SDK_PATH TEST_PATH
Run unit test for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):

    # Setup path to GAE libs
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Run in dev environment
    os.environ['SERVER_SOFTWARE'] = 'Dev-XXX'

    # Find tests and run them
    suite = unittest.loader.TestLoader().discover(test_path, pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print 'Error: Exactly 2 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    main(SDK_PATH, TEST_PATH)