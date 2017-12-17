#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing DocumentStorer class.
"""

from src.models.document_model import DocumentModel
from elasticsearch import Elasticsearch
from typing import Union


class DocumentStorer(object):
    """
    This class is used as an interface for storing and retrieving a document through its model.
    """
    def __init__(self, es: Elasticsearch) -> None:
        self.es = es
        self.hits_models = []

    def store(self, dm: DocumentModel, doc_id=None):
        """
        Store a document model.
        :param dm: Document model to be stored
        :param doc_id: ID of the document
        :return: store result
        """
        body = dm.render_for_store()

        res = self.es.index('docs', 'doc', body, id=doc_id)
        dm.id = res['_id']

    def update(self, dm: DocumentModel, om: DocumentModel):
        """
        Update a document in the store, updating document within the "docs" index, and creating a document with old
        values in the "docs_history" index.
        :param dm: Up-to-date model
        :param om: Model containing deprecated values
        :return:
        """
        dm_body = dm.render_for_store()

        self.es.update('docs', 'doc', dm.id.value, {'doc': dm_body})

        om_body = om.render_for_store()

        self.es.index('docs_history', 'doc', {'doc': om_body})

    def retrieve(self, doc_id: str) -> DocumentModel:
        """
        Retrieve document from store.
        :param doc_id: ID of the document
        :return: The document model.
        """
        res = self.es.get('docs', doc_id, 'doc')
        dm = DocumentModel()

        dm.id.value = doc_id
        dm.set_from_store(res['_source'])

        return dm

    def _search_term(self, terms: dict, index: str='docs') -> None:
        body = {'query': {'term': terms}}
        self._search(body, index)

    def _search(self, body: dict, index: str='docs'):
        res = self.es.search(index, 'doc', body)
        for hit in res['hits']['hits']:
            dm = DocumentModel()

            dm.id.value = hit['_id']
            dm.set_from_store(hit['_source'])
            self.hits_models.append(dm)

    def search_all(self):
        self._search({})

    def search_url(self, url):
        self._search_term({'url': url})

    def retrieve_old_versions(self, doc_id):
        self._search_term({'doc_youngest_id': doc_id}, index='docs_history')
