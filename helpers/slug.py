# -*- coding: utf-8 -*-
#
# Methods to help work with URL slugs
#

import re
import unicodedata

class SlugError(Exception):
    """ A slug generation exception """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


def create(string):
    """ Attempts to create a valid url slug from string """
    if not isinstance(string, str) and not isinstance(string, unicode):
        raise ValueError("Input must be a non-empty string")

    if len(string) == 0:
        raise ValueError("Input must be a non-empty string")

    string = unicodedata.normalize('NFD', unicode(string)).encode('ascii', 'ignore')
    string = re.sub(r'[^a-zA-Z0-9\_]', ' ', string).strip()
    slug = re.sub(r'\s+', '-', string).lower()

    if len(slug) < 3:
        raise SlugError("Generated slug must be at least 3 characters long")

    return slug


def validate(string):
    """ Validates that string is formatted like a url slug """
    regex = re.compile('^[a-z0-9\-\_]{3,}$')
    return regex.match(string)