# -*- coding: utf-8 -*-
#
# Wrappers for working with the search index
#
from google.appengine.api import search
import logging

_OPEN_DATA_INDEX = 'open_data_index'


def query(query=u""):
    """Search the document index"""
    logging.info("Searching with query: %s" % query)

    try:
        index = search.Index(name=_OPEN_DATA_INDEX)
        query_options = search.QueryOptions(ids_only=True)
        return index.search(search.Query(query_string=query, options=query_options))
    
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


def empty_index():
    """Reindex all documents from scratch"""
    logging.info("Attempting to delete all entries from search index")

    index = search.Index(name=_OPEN_DATA_INDEX)

    while True:
        document_ids = [doc.doc_id for doc in index.get_range(ids_only=True)]

        if not document_ids:
            break

        index.delete(document_ids)