# -*- coding: utf-8 -*-
import os
import re
import unittest
from helpers import slug


class SlugTest(unittest.TestCase):


    def test_slug_create(self):

        # Requires non-empty str
        with self.assertRaises(ValueError): slug.create(None)
        with self.assertRaises(ValueError): slug.create(0)
        with self.assertRaises(ValueError): slug.create(True)
        with self.assertRaises(ValueError): slug.create(False)
        with self.assertRaises(ValueError): slug.create(0.0)
        with self.assertRaises(ValueError): slug.create("")

        # Generated slug must be at least 3 characters long
        with self.assertRaises(slug.SlugError): slug.create("a")
        with self.assertRaises(slug.SlugError): slug.create("ab")
        with self.assertRaises(slug.SlugError): slug.create("ab!")

        # (input_string, output_string)
        strings_to_test = [
            ('abc123',   'abc123'),
            ('ABC123',   'abc123'),
            ('abc123 ',  'abc123'),
            (' abc123',  'abc123'),
            ('ab c12 3', 'ab-c12-3'),
            (u'Áßç123',  'ac123'),
        ]

        # Friendly URL regex
        regex = re.compile('^[a-z0-9\-\_]{3,}$')

        # Test a series of string conversions
        for in_str, out_str in strings_to_test:
            my_slug = slug.create(in_str)
            msg = "Failed with string '%s' desired: '%s' actual: '%s'" % (in_str, out_str, my_slug)
            self.assertIsInstance(my_slug, str, msg=msg)
            self.assertTrue(len(my_slug)>0, msg=msg)
            self.assertTrue(regex.match(my_slug), msg=msg)
            self.assertEqual(my_slug, out_str, msg=msg)



    def test_slug_validate(self):

        self.assertFalse(slug.validate(" abc123"))
        self.assertFalse(slug.validate("abc123 "))
        self.assertFalse(slug.validate("abc 123"))
        self.assertFalse(slug.validate("abc!123"))
        self.assertFalse(slug.validate("!!!"))
        self.assertFalse(slug.validate("a"))
        self.assertFalse(slug.validate("ab"))

        self.assertTrue(slug.validate("abc"))
        self.assertTrue(slug.validate("abc123"))
        self.assertTrue(slug.validate("abc-123"))
        self.assertTrue(slug.validate("abc_123"))
