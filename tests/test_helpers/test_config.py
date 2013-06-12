# -*- coding: utf-8 -*-
import os
import unittest
from helpers.config import load_config


class LoadConfigTest(unittest.TestCase):

    def test_development_config(self):
        os.environ['SERVER_SOFTWARE'] = 'Dev-XXX'
        debug, config = load_config()
        self.assertIsInstance(debug, bool)
        self.assertIsInstance(config, dict)
        self.assertTrue(debug)

    def test_production_config(self):
        os.environ['SERVER_SOFTWARE'] = 'Live-XXX'
        debug, config = load_config()
        self.assertIsInstance(debug, bool)
        self.assertIsInstance(config, dict)
        self.assertFalse(debug)