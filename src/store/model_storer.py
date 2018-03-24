#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing Store methods.
"""

from src.models.document_model import DocumentModel, OldDocumentModel
from src.store.elastic import es, DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
from elasticsearch.exceptions import NotFoundError
from src.heraldic_exceptions import DocumentNotChangedException
from typing import List


def store(dm: DocumentModel, doc_id=None):
    """
    Store a document model.
    :param dm: Document model to be stored
    :param doc_id: ID of the document
    :return: store result
    """
    body = dm.render_for_store()

    res = es.index(DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME, body=body, id=doc_id)
    doc_id = res['_id']
    es.indices.refresh(index=DocumentIndex.INDEX_NAME)

    if dm.has_errors:
        errors_body = dm.render_errors_for_store()

        es.index(ErrorIndex.INDEX_NAME, doc_type=ErrorIndex.TYPE_NAME, body=errors_body, id=doc_id)
        es.indices.refresh(index=ErrorIndex.INDEX_NAME)

    if dm.has_suggestions:
        suggestions_body = dm.render_suggestions_for_store()

        es.index(SuggestionIndex.INDEX_NAME, doc_type=SuggestionIndex.TYPE_NAME, body=suggestions_body, id=doc_id)
        es.indices.refresh(index=SuggestionIndex.INDEX_NAME)

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
            es.index(SuggestionIndex.INDEX_NAME, doc_type=SuggestionIndex.TYPE_NAME, body=suggestions_body,
                     id=dm.id.value)
            es.indices.refresh(index=SuggestionIndex.INDEX_NAME)
        else:
            try:
                es.delete(SuggestionIndex.INDEX_NAME, doc_type=SuggestionIndex.TYPE_NAME, id=dm.id.value)
            except NotFoundError:
                pass

        if dm.has_errors:
            errors_body = dm.render_errors_for_store()
            es.index(ErrorIndex.INDEX_NAME, ErrorIndex.TYPE_NAME, body=errors_body, id=dm.id.value)
            es.indices.refresh(index=ErrorIndex.INDEX_NAME)
        else:
            try:
                es.delete(ErrorIndex.INDEX_NAME, doc_type=ErrorIndex.TYPE_NAME, id=dm.id.value)
            except NotFoundError:
                pass
    if dm.storable_values_updated:
        dm_body = dm.render_for_store()
        es.update(DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME, id=dm.id.value,
                  body={'doc': dm_body})

        om_body = om.render_for_store()
        es.index(OldVersionIndex.INDEX_NAME, doc_type=OldVersionIndex.TYPE_NAME, body=om_body)
        es.indices.refresh(index=OldVersionIndex.INDEX_NAME)
    else:
        raise DocumentNotChangedException


def delete(dm: DocumentModel, old_models: List[DocumentModel]) -> None:
    es.delete(DocumentIndex.INDEX_NAME, id=dm.id, doc_type=DocumentIndex.TYPE_NAME)
    es.indices.refresh(index=DocumentIndex.INDEX_NAME)

    if dm.has_suggestions:
        es.delete(SuggestionIndex.INDEX_NAME, id=dm.id, doc_type=SuggestionIndex.TYPE_NAME)
        es.indices.refresh(index=SuggestionIndex.INDEX_NAME)

    if dm.has_errors:
        es.delete(ErrorIndex.INDEX_NAME, id=dm.id, doc_type=ErrorIndex.TYPE_NAME)
        es.indices.refresh(index=ErrorIndex.INDEX_NAME)

    for old_dm in old_models:
        es.delete(OldVersionIndex.INDEX_NAME, id=old_dm.id, doc_type=OldVersionIndex.TYPE_NAME)

    es.indices.refresh(index=OldVersionIndex.INDEX_NAME)


def store_feed(body: dict):
    es.index(FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME, body=body)


def update_feed(feed_id, body):
    es.update(FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME, id=feed_id, body={'doc': body})
