# -*- coding: utf-8 -*-
import os
import unittest
from helpers.config import load_config


class LoadConfigTest(unittest.TestCase):

    def test_development_config(self):
        os.environ['SERVER_SOFTWARE'] = 'Dev-XXX'
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertTrue(config['debug'])

    def test_production_config(self):
        os.environ['SERVER_SOFTWARE'] = 'Live-XXX'
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertFalse(config['debug'])