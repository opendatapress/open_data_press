# -*- coding: utf-8 -*-
#
# Dummy parameters for models created in unit tests
#

from datetime import datetime

credentials = '''{
  "invalid": false,
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "refresh_token": "",
  "client_id": "351298984682.apps.googleusercontent.com",
  "token_expiry": "2050-11-14T11:26:32Z",
  "user_agent": null,
  "access_token": "ya29.1.AADtN_VSDGUctyiNf8Ls6ZAHvLlmti1OIYbxAUalbUWN7N0ooFMeSl03AqlC8SeoacLgNA",
  "client_secret": "m_QLqYSZHe_GqlqS22rEtwDq"
}'''

# Params for a valid user record
user = {
        'created_at':          datetime.now(),
        'credentials':         credentials,
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
    'created_at':  datetime.now(),
    'modified_at': datetime.now(),
    'extension':   u'txt',
    'mimetype':    u'text/plain'
}