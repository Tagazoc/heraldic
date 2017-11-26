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

    def store(self, dm: DocumentModel, doc_id=None) -> int:
        """
        Store a document model.
        :param dm: Document model to be stored
        :param doc_id: ID of the document
        :return: store result
        """
        body = {}
        for k, v in dm.attributes.items():
            if v.storable:
                body[k] = v.render_for_store()

        res = self.es.index('docs', 'doc', body, id=doc_id)
        dm.id = res['_id']
        return res['result'] == 'created'

    def search(self, url) -> int:
        # TODO
        res = self.es.search('docs', 'doc', url)
        return res

    def update(self, dm: DocumentModel):
        # TODO pour chaque attribut mis à jour, on récupère l'ancienne valeur qu'on place dans un nouveau document dans
        # l'index doc_history
        # Puis on met à jour le document actuel en incrémentant la version
        pass

    def retrieve(self, doc_id) -> DocumentModel:
        """
        Retrieve document from store.
        :param doc_id: ID of the document
        :return: The document model.
        """
        res = self.es.get('docs', doc_id, 'doc')
        dm = DocumentModel()

        dm.id.value = doc_id
        for k, v in dm.attributes.items():
            if v.storable:
                v.update_from_store(res['_source'][k])

        dm.id = doc_id

        return dm
