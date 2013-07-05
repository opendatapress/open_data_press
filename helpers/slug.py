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
    string = re.sub(r'[^a-zA-Z0-9]', ' ', string).strip()
    return re.sub(r'\s+', '-', string).lower()


def validate(string):
    return True