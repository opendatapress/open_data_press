# -*- coding: utf-8 -*-
#
# Methods to help work with URL slugs
#

import re
import unicodedata

def create(string):
    if not isinstance(string, str) and not isinstance(string, unicode):
        raise ValueError("Input must be a non-empty string")

    if len(string) == 0:
        raise ValueError("Input must be a non-empty string")

    string = unicodedata.normalize('NFD', unicode(string)).encode('ascii', 'ignore')
    string = re.sub(r'[^a-zA-Z0-9\_]', ' ', string).strip()
    slug = re.sub(r'\s+', '-', string).lower()

    if len(slug) < 3:
        raise ValueError("Generated slug must be at least 3 characters long")

    return slug


def validate(string):
    # TODO
    return True