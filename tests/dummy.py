# -*- coding: utf-8 -*-
#
# Dummy parameters for models created in unit tests
#

from datetime import datetime

# Params for a valid user record
user = {
        'created_at':          datetime.now(),
        'credentials':         '{"token":"XXX"}',
        'google_birthday':     u'0000-01-01',
        'google_email':        u'test.user@gmail.com',
        'google_gender':       u'male',
        'google_id':           u'123456789',
        'google_locale':       u'en-GB',
        'google_name':         u'Test User',
        'google_picture_url':  u'https://lh3.googleusercontent.com/image.png',
        'last_login_at':       datetime.now(),
        'modified_at':         datetime.now(),
        'profile_email':       u'test.user@email.com',
        'profile_description': u'This is a test user account',
        'profile_name':        u'Test User',
        'profile_slug':        'test-user',
        'profile_web_address': 'http://test-user.com',
    }

# Params for a valid data source record
# Except for DataSource.user which must be defined within tests
data_source = {
    'created_at':         datetime.now(),
    'description':        u'A Dummy Data Source',
    'google_spreadsheet': u'dummy_key',
    'google_worksheet':   u'dummy_id',
    'licence':            u'Do What You Like',
    'modified_at':        datetime.now(),
    'slug':               u'data-1',
    'tags':               u'Apples, Oranges, Pears',
    'tbl_stars':          5,
    'title':              u'Dummy Data',
}

data_source_json = {
    'description':        u'A Dummy Data Source',
    'google_spreadsheet': u'dummy_key',
    'google_worksheet':   u'dummy_id',
    'licence':            u'Do What You Like',
    'slug':               u'data-1',
    'tags':               u'Apples, Oranges, Pears',
    'tbl_stars':          5,
    'title':              u'Dummy Data',
}


# Params for valid data view model
data_view = {
    'created_at':         datetime.now(),
    'modified_at':        datetime.now(),
}