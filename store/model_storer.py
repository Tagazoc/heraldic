#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing Store methods.
"""

from src.models.document_model import DocumentModel, OldDocumentModel
from src.store.elastic import es


def store(dm: DocumentModel, doc_id=None):
    """
    Store a document model.
    :param dm: Document model to be stored
    :param doc_id: ID of the document
    :return: store result
    """
    body = dm.render_for_store()

    res = es.index('docs', 'doc', body, id=doc_id)
    dm.id = res['_id']


def update(dm: DocumentModel, om: OldDocumentModel):
    """
    Update a document in the store, updating document within the "docs" index, and creating a document with old
    values in the "docs_history" index.
    :param dm: Up-to-date model
    :param om: Model containing deprecated values
    :return:
    """
    dm_body = dm.render_for_store()

    es.update('docs', 'doc', dm.id.value, {'doc': dm_body})

    om_body = om.render_for_store()

    es.index('docs_history', 'doc', om_body)
