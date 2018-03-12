#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing Store methods.
"""

from src.models.document_model import DocumentModel, OldDocumentModel
from src.store.elastic import es
from elasticsearch.exceptions import NotFoundError
from src.heraldic_exceptions import DocumentNotChangedException


def store(dm: DocumentModel, doc_id=None):
    """
    Store a document model.
    :param dm: Document model to be stored
    :param doc_id: ID of the document
    :return: store result
    """
    body = dm.render_for_store()

    res = es.index('docs', 'doc', body, id=doc_id)
    doc_id = res['_id']

    if dm.has_errors:
        errors_body = dm.render_errors_for_store()

        es.index('errors', 'doc_errors', errors_body, id=doc_id)

    if dm.has_suggestions:
        suggestions_body = dm.render_suggestions_for_store()

        es.index('suggestions', 'doc', suggestions_body, id=doc_id)

    return doc_id


def update(dm: DocumentModel, om: OldDocumentModel):
    """
    Update a document in the store, updating document within the "docs" index, and creating a document with old
    values in the "docs_history" index.
    :param dm: Up-to-date model
    :param om: Model containing deprecated values
    :return:
    """

    if dm.from_gathering:
        if dm.has_suggestions:
            suggestions_body = dm.render_suggestions_for_store()
            es.index('suggestions', 'doc', suggestions_body, id=dm.id.value)
        else:
            try:
                es.delete('suggestions', 'doc', dm.id.value)
            except NotFoundError:
                pass

        if dm.has_errors:
            errors_body = dm.render_errors_for_store()
            es.index('errors', 'doc_errors', errors_body, id=dm.id.value)
        else:
            try:
                es.delete('errors', 'doc_errors', dm.id.value)
            except NotFoundError:
                pass
    if dm.storable_values_updated:
        dm_body = dm.render_for_store()
        es.update('docs', 'doc', dm.id.value, {'doc': dm_body})

        om_body = om.render_for_store()
        es.index('docs_history', 'doc', om_body)
    else:
        raise DocumentNotChangedException
