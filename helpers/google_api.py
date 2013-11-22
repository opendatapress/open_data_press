# -*- coding: utf-8 -*-
#
# A wrappers and helpers for working with Google APIs
#

import httplib2
import re
import logging
import unicodedata
import base64
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from helpers.config import load_config, ConfigurationError
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client.anyjson import simplejson as json
from apiclient.discovery import build


class GoogleAPIException(Exception):
    pass

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
    http  = httplib2.Http(timeout=30)
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
#  page_token: a b64 encoded token to fetch the next page in the file sequence
#
def list_drive_files(auth_json, query="", page_token=None):
    try:
        http = http_from_oauth2(auth_json)
        service = drive_service()
        file_list = []
        param = {'q': query, 'maxResults': 25}
        if page_token:
            param['pageToken'] = base64.b64decode(page_token)

        files = service.files().list(**param).execute(http=http)

        file_list.extend(files['items'])
        next_page_token = files.get('nextPageToken')
        next_page_url = None

        if next_page_token:
            next_page_token = base64.b64encode(next_page_token)
            next_page_url   = "/api/0/google/sheets?page_token=%s" % next_page_token

        return {
            'files':           file_list,
            'num_files':       len(file_list), 
            'next_page_url':   next_page_url, 
            'next_page_token': next_page_token
        }

    except UnicodeDecodeError as e:
        logging.error(e)
        raise GoogleAPIException('Could not fetch file list from Google Drive - Invalid Page Token')

    except Exception as e:
        logging.error(e)
        raise GoogleAPIException('Could not fetch file list from Google Drive - Unknown Error')


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
        raise GoogleAPIException(msg)

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
        return data

    except Exception as e:
        raise GoogleAPIException('Could not parse spreadsheet data from Google.')



# Get all the data in a worksheet
#  auth_json        A JSON object of valid credentials
#  spreadsheet_key  Identifier for the spreadsheet 
#  worksheet_key    Identifier for the worksheet
#  limit            The maximum number of data rows to return
# 
def get_cell_data(auth_json, spreadsheet_key, worksheet_key, limit=None):
    http = http_from_oauth2(auth_json)
    uri = 'https://spreadsheets.google.com/feeds/list/%s/%s/private/full' % (spreadsheet_key, worksheet_key)
    response = http.request(uri)

    limit = limit if isinstance(limit, int) else 200000

    if "The spreadsheet at this URL could not be found" in response[1]:
        msg = "The worksheet with this id <%s> cannot be found. Make sure the owner of the spreadsheet hasn't deleted it." % spreadsheet_key
        raise GoogleAPIException(msg)

    if "Invalid query parameter value for grid-id." in response[1]:
        msg = "The worksheet with this id <%s> cannot be found. Make sure the ownder of the spreadsheet hasn't deleted it." % worksheet_key
        raise GoogleAPIException(msg)

    try:
        # Attempt to parse response
        feed = ET.fromstring(response[1])

        # XML Prefixes
        atom   = '{http://www.w3.org/2005/Atom}'
        search = '{http://a9.com/-/spec/opensearchrss/1.0/}'
        gsx    = '{http://schemas.google.com/spreadsheets/2006/extended}'

        # Format worksheet data
        data = {
            'key':           spreadsheet_key,
            'id':            worksheet_key,
            'title':         _val(feed.find('%stitle' % atom).text),
            'updated':       _val(feed.find('%supdated' % atom).text),
            'start_index':   _val(feed.find('%sstartIndex' % search).text),
            'author': {
                'name':      _val(feed.find('.//%sname' % atom).text),
                'email':     _val(feed.find('.//%semail' % atom).text),
            },
            'data_rows':     [],
            'headings':      [],
        }

        # Format cell data
        for entry in feed.findall('%sentry' % atom):
            if len(data['data_rows']) < limit:
                row = {}
                for field in entry:
                    if gsx in field.tag:
                        row[_key(field.tag)] = _val(field.text)
                data['data_rows'].append(row)

        data['total_results'] = len(data['data_rows'])

        if len(data['data_rows']):
            data['headings'] = [h for h in data['data_rows'][0].keys()]
            
        return data

    except Exception as e:
        raise GoogleAPIException('Could not parse spreadsheet data from Google.')


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
# Normaises dates and times to "YYYY-MM-DD HH-MM-SS" format 
# including with millisecond precision if available
#
#  value: str/unicode
#                          .__
#  Also: Skiing :)         |__]
#                          |
#                          |
#                          |                              _
def _val(val):    #::::....|...                       ___(_)
    if val is None: return ""  #:.                   /  / /\
    try: return int(val)          #:.               /   `\\ |
    except ValueError:               #:.               \\// |
        try:                            #:.             \\\
            return float(val)              #:.           \\\
        except ValueError:                     #:.        ``
            try:                                   #:.                         ^
                return str(dt.strptime(val,"%H:%M:%S"))#:.                     ^
            except ValueError:                            #:.                 ^^^
                try:                                         #:.              ^^^
                    return str(dt.strptime(val, "%d/%m/%Y"))    #:.          ^^^^^
                except ValueError:                                 #:.      ^^^^^^^
                    try:                                              #:.      |
                        return str(dt.strptime(val, "%d/%m/%Y %H:%M:%S")) #:.  |                  .__
                    except ValueError:                                       #:.                  |__]
                        try:                                                     #:.              |
                            return str(dt.strptime(val[0:23], "%Y-%m-%dT%H:%M:%S.%f"))#:.         |
                        except ValueError:                                                #:..    |
                            return val                                                         #:.|..