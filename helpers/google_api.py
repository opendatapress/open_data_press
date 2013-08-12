# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

import httplib2
import re
import logging
import unicodedata
from datetime import datetime
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
        msg = "The worksheet with this id <%s> cannot be found. Make sure the owner of the spreadsheet hasn't deleted it." % spreadsheet_key
        return {'response': 'error', 'body': msg}

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
            'title':         _val(feed.find('%stitle' % atom).text),
            'updated':       _val(feed.find('%supdated' % atom).text),
            'total_results': _val(feed.find('%stotalResults' % search).text),
            'start_index':   _val(feed.find('%sstartIndex' % search).text),
            'author': {
                'name':      _val(feed.find('.//%sname' % atom).text),
                'email':     _val(feed.find('.//%semail' % atom).text),
            },
            'worksheets':    [],
        }
        
        # Format worksheet data
        for entry in feed.findall('%sentry' % atom):
            worksheet = {
                'id':        re.sub('^.*full/','',entry.find('%sid' % atom).text),
                'title':     _val(entry.find('%stitle' % atom).text),
                'updated':   _val(entry.find('%supdated' % atom).text),
                'row_count': _val(entry.find('%srowCount' % gs).text),
                'col_count': _val(entry.find('%scolCount' % gs).text),
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
    http = http_from_oauth2(auth_json)
    uri = 'https://spreadsheets.google.com/feeds/list/%s/%s/private/full' % (spreadsheet_key, worksheet_key)
    response = http.request(uri)

    if "The spreadsheet at this URL could not be found" in response[1]:
        msg = "The worksheet with this id <%s> cannot be found. Make sure the owner of the spreadsheet hasn't deleted it." % spreadsheet_key
        return {'response': 'error', 'body': msg}

    if "Invalid query parameter value for grid-id." in response[1]:
        msg = "The worksheet with this id <%s> cannot be found. Make sure the ownder of the spreadsheet hasn't deleted it." % worksheet_key
        return {'response': 'error', 'body': msg}

    try:
        # Attempt to parse response
        feed = ET.fromstring(response[1])

        # XML Prefixes
        atom   = '{http://www.w3.org/2005/Atom}'
        search = '{http://a9.com/-/spec/opensearchrss/1.0/}'
        gsx    = '{http://schemas.google.com/spreadsheets/2006/extended}'

        # Format worksheet data
        data = {
            'spreadsheet_key': spreadsheet_key,
            'worksheet_key':   worksheet_key,
            'title':           _val(feed.find('%stitle' % atom).text),
            'updated':         _val(feed.find('%supdated' % atom).text),
            'total_results':   _val(feed.find('%stotalResults' % search).text),
            'start_index':     _val(feed.find('%sstartIndex' % search).text),
            'author': {
                'name':        _val(feed.find('.//%sname' % atom).text),
                'email':       _val(feed.find('.//%semail' % atom).text),
            },
            'data_rows':       [],
        }

        # Format cell data
        for entry in feed.findall('%sentry' % atom):
            row = {}
            for field in entry:
                if gsx in field.tag:
                    row[_key(field.tag)] = _val(field.text)
            data['data_rows'].append(row)

    except Exception as e:
        return {'response': 'error', 'body': 'Could not parse spreadsheet data from Google.'}

    return {'response': 'success', 'body': data}


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


# Convert potentially unfriendly column headings in to friendly headings
#  heading: Str
def _key(heading):
    # Strip XML namespace    
    gsx = '{http://schemas.google.com/spreadsheets/2006/extended}'
    heading = heading.replace(gsx, '')
    # Convert accented letter to ASCII lower-case equivalents
    return unicodedata.normalize('NFD', unicode(heading)).encode('ascii', 'ignore')


# Convert cell values to int or float if possible
# Also normaises dates and times to "YYYY-MM-DD HH-MM-SS" format 
# including with millisecond precision if available
#  value: str/unicode
def _val(value):
    if value is None: return ""
    try: return int(value)
    except ValueError:
        try: return float(value)
        except ValueError:
            try: return str(datetime.strptime(value[0:23], "%Y-%m-%dT%H:%M:%S.%f"))
            except ValueError:
                try: return str(datetime.strptime(value, "%d/%m/%Y %H:%M:%S"))
                except ValueError:
                    try: return str(datetime.strptime(value, "%d/%m/%Y"))
                    except ValueError:
                        try: return str(datetime.strptime(value, "%H:%M:%S"))
                        except ValueError:
                            return value
