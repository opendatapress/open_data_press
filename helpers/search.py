# -*- coding: utf-8 -*-
#
# Wrappers for working with the search index
#
from google.appengine.api import search
import logging

_OPEN_DATA_INDEX = 'open_data_index'

def query(query=u""):
    """Search the document index"""
    logging.info("Searching: %s" % query)

    try:
        index = search.Index(name=_OPEN_DATA_INDEX)
        return index.search(query)
    
    except search.Error as e:
        logging.exception("Failed to search index: %s" % e)


def index_doc(document=None):
    """Add/update a document in the search index"""
    logging.info("Attempting to index document %s" % document)

    try:
        index = search.Index(name=_OPEN_DATA_INDEX)
        index.put(document)
    
    except search.Error as e:
        logging.exception('Failed to index document: %s' % e)


def delete_doc(doc_id=''):
    """Delete a document from the search index"""
    logging.info("Attempting to delete document with id %s" % doc_id)

    try:
        index = search.Index(name=_OPEN_DATA_INDEX)
        index.delete(doc_id)
    
    except search.Error as e:
        logging.exception('Failed to delete document: %s' % e)


def rebuild_index():
    """Reindex all documents from scratch"""
    # TODO: Admin method to rebuild search index #issue37
    pass