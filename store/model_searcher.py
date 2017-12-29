#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing ModelSearcher class.
"""

from elasticsearch import Elasticsearch
from src.models.document_model import DocumentModel


class ModelSearcher(object):
    """
        This class is used as an interface for storing and retrieving a document through its model.
    """

    def __init__(self, es: Elasticsearch) -> None:
        self.es = es
        self.hits_models = []

    def _search_term(self, terms: dict, index: str='docs', limit=0) -> None:
        body = {'query': {'term': terms}}
        if limit:
            # body['terminate_after'] = limit
            pass
        self._search(body, index)

    def _search(self, body: dict, index: str='docs'):
        res = self.es.search(index, 'doc', body)
        for hit in res['hits']['hits']:
            dm = DocumentModel()

            dm.id.value = hit['_id']
            dm.set_from_store(hit['_source'])
            self.hits_models.append(dm)

    def search_all_docs(self):
        self._search({})

    def search_url(self, url):
        self._search_term({'url': url}, limit=1)

    def retrieve_old_versions(self, doc_id):
        self._search_term({'doc_youngest_id': doc_id}, index='docs_history')
