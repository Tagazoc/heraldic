#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing DocumentStorer class.
"""

from src.models.document_model import DocumentModel
from src.store.model_searcher import ModelSearcher
from elasticsearch import Elasticsearch
from src.heraldic_exceptions import DocumentNotFoundException


class DocumentStorer(object):
    """
    This class is used as an interface for storing and retrieving a document through its model.
    """
    def __init__(self, es: Elasticsearch) -> None:
        self.es = es

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

    def retrieve_from_url(self, url: str) -> DocumentModel:
        ms = ModelSearcher(self.es)
        ms.search_url(url)
        try:
            return ms.hits_models[0]
        except IndexError:
            raise DocumentNotFoundException
