# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

import httplib2
import re
import logging
import xml.etree.ElementTree as ET
from helpers.config import load_config, ConfigurationError
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client.anyjson import simplejson as json
from apiclient.discovery import build


# An oAuth2 authentication flow handler
def oauth2_flow(**kwargs):
    config = load_config()
    try:
        return OAuth2WebServerFlow(
            client_id     = config['google_api']['client_id'],
            client_secret = config['google_api']['client_secret'],
            scope         = " ".join(config['google_api']['scopes']),
            redirect_uri  = config['google_api']['redirect_uri'],
            **kwargs)
    except KeyError as e:
        raise ConfigurationError("Missing required configuration parameter %s" % e)


# Get an HTTP client authorised with oAuth2 credentials json
#
#  auth_json : a JSON object of valid credentials
#
def http_from_oauth2(auth_json):
    http  = httplib2.Http()
    creds = OAuth2Credentials.from_json(auth_json)
    return creds.authorize(http)


# Get user information using credentials json
#
#  auth_json : a JSON object of valid credentials
#
def user_info(auth_json):
    http = http_from_oauth2(auth_json)
    response = http.request('https://www.googleapis.com/oauth2/v2/userinfo')
    return json.loads(response[1])


# Set API client access to the drive API
def drive_service():
    return build('drive', 'v2')


# Get a list of files from Google Drive
# See: https://developers.google.com/drive/search-parameters
#
#  auth_json : a JSON object of valid credentials
#  query     : A search query string for the files API
#
def list_drive_files(auth_json, query=""):
    http = http_from_oauth2(auth_json)
    service = drive_service()
    file_list = []
    page_token = None
    while True:
        param = {'q': query}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute(http=http)
        file_list.extend(files['items'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    data = {'num_files': len(file_list), 'files':file_list}
    return {'response':'success', 'body': data}


# Get a list of all the worksheets in a spreadsheet
#  auth_json      : a JSON object of valid credentials
#  spreadsheet_key : Identifier for the spreadsheet 
# 
def get_worksheets(auth_json, spreadsheet_key):
    http = http_from_oauth2(auth_json)
    uri = 'https://spreadsheets.google.com/feeds/worksheets/%s/private/full' % spreadsheet_key
    response = http.request(uri)

    if "The spreadsheet at this URL could not be found" in response[1]:
        return {'response': 'error', 'body': response[1]}

    try:
        # Attempt to parse response
        feed = ET.fromstring(response[1])

        # XML Prefixes
        atom    = '{http://www.w3.org/2005/Atom}'
        search  = '{http://a9.com/-/spec/opensearchrss/1.0/}'
        gs      = '{http://schemas.google.com/spreadsheets/2006}'

        # Format spreadsheet data
        data = {
            'key':           spreadsheet_key,
            'title':         feed.find('%stitle' % atom).text,
            'updated':       feed.find('%supdated' % atom).text,
            'total_results': int(feed.find('%stotalResults' % search).text),
            'start_index':   int(feed.find('%sstartIndex' % search).text),
            'author': {
                'name':      feed.find('.//%sname' % atom).text,
                'email':     feed.find('.//%semail' % atom).text,
            },
            'worksheets':    [],
        }
        
        # Format worksheet data
        for entry in feed.findall('%sentry' % atom):
            worksheet = {
                'id':        re.sub('^.*full/','',entry.find('%sid' % atom).text),
                'title':     entry.find('%stitle' % atom).text,
                'updated':   entry.find('%supdated' % atom).text,
                'row_count': int(entry.find('%srowCount' % gs).text),
                'col_count': int(entry.find('%scolCount' % gs).text),
            }
            data['worksheets'].append(worksheet)

        # Return structured data
        return {'response': 'success', 'body': data}

    except Exception as e:
        return {'response': 'error', 'body': 'Could not parse spreadsheet data from Google.'}



# Get all the data in a worksheet
#  auth_json      : a JSON object of valid credentials
#  spreadsheet_key : Identifier for the spreadsheet 
#  worksheet_key  : Identifier for the worksheet
# 
def get_cell_data(auth_json, spreadsheet_key, worksheet_key):
    pass


# Create a spreadsheet file in Drive
#  auth_json : a JSON object of valid credentials
#  title     : the title for the file
#
def create_spreadsheet(auth_json, title=""):
    pass


# Create a new worksheet in a spreadsheet
#  auth_json : a JSON object of valid credentials
#  spreadsheet_key : Identifier for the spreadsheet
#
def create_worksheet(auth_json, spreadsheet_key):
    pass


# Save data in to a worksheet
#  auth_json : a JSON object of valid credentials
#  spreadsheet_key : Identifier for the spreadsheet 
#  worksheet_key  : Identifier for the worksheet
#  data           : 2-D array of cell data - [row [column]]
def save_data(auth_json, spreadsheet_key, worksheet_key, data=[[]]):
    pass