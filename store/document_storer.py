#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used for HTML document.
"""

from src.models.document_model import DocumentModel
from elasticsearch import Elasticsearch
from datetime import datetime


class DocumentStorer(object):
    def __init__(self, hosts=None, **kwargs):
        self.es = Elasticsearch(hosts, **kwargs)

    def store(self, dm: DocumentModel, doc_id=None) -> bool:
        """
        Store a document model.
        :param dm: Document model to be stored
        :param doc_id: ID of the document
        :return: store result
        """
        body = {
            "title": dm.title,
            "description": dm.description,
            "url": dm.url,
            "media": dm.media,
            "gather_timestamp": round(dm.gather_time.timestamp()),
            "update_timestamp": round(dm.update_time.timestamp()),
            "doc_publication_timestamp": round(dm.doc_publication_time.timestamp()),
            "doc_update_timestamp": round(dm.doc_update_time.timestamp()),
            "category": dm.category,
            "quotes": dm.quotes,
            "href_sources": dm.href_sources,
            "explicit_sources": dm.explicit_sources
        }

        res = self.es.index('docs', 'doc', body, id=doc_id)
        return res['created']

    def retrieve(self, doc_id) -> DocumentModel:
        """
        Retrieve document from store.
        :param doc_id: ID of the document
        :return: The document model.
        """
        res = self.es.get('docs', doc_id, 'doc')
        dm = DocumentModel()
        dm.url = res['url']
        dm.title = res['title']
        dm.description = res['description']
        dm.media = res['media']
        dm.gather_time = datetime.fromtimestamp(res['gather_timestamp'])
        dm.doc_publication_time = datetime.fromtimestamp(res['publication_timestamp'])
        dm.doc_update_time = datetime.fromtimestamp(res['update_timestamp'])
        dm.category = res['category']
        dm.quotes = res['quotes']
        dm.href_sources = res['href_sources']
        dm.explicit_sources = res['explicit_sources']
        dm.id = doc_id

        return dm
