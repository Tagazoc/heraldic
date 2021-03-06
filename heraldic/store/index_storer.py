#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing Store methods.
"""

from heraldic.models.document_model import DocumentModel, OldDocumentModel
from heraldic.store.elastic import es, DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
from elasticsearch.exceptions import NotFoundError
import heraldic.misc.functions as functions
from heraldic.misc.exceptions import DocumentNotChangedException
from typing import List


@functions.handle_connection_errors
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
    elif doc_id is not None:
        # If doc_id is not None, it may be because a parsing error already exists
        delete_error(doc_id)

    if dm.has_suggestions:
        suggestions_body = dm.render_suggestions_for_store()

        es.index(SuggestionIndex.INDEX_NAME, doc_type=SuggestionIndex.TYPE_NAME, body=suggestions_body, id=doc_id)
        es.indices.refresh(index=SuggestionIndex.INDEX_NAME)

    return doc_id


@functions.handle_connection_errors
def store_failed_parsing_error(dm: DocumentModel, doc_id=None):
    errors_body = dm.render_errors_for_store()
    es.index(ErrorIndex.INDEX_NAME, doc_type=ErrorIndex.TYPE_NAME, body=errors_body, id=doc_id)
    es.indices.refresh(index=ErrorIndex.INDEX_NAME)


@functions.handle_connection_errors
def delete_error(doc_id):
    try:
        es.delete(ErrorIndex.INDEX_NAME, doc_type=ErrorIndex.TYPE_NAME, id=doc_id)
        es.indices.refresh(index=ErrorIndex.INDEX_NAME)
    except NotFoundError:
        pass


@functions.handle_connection_errors
def update(dm: DocumentModel, om: OldDocumentModel, update_inplace=False):
    """
    Update a document in the store, updating document within the "docs" index, and creating a document with old
    values in the "docs_history" index.
    :param update_inplace: Whether we add old model to versions of the document
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
                es.indices.refresh(index=SuggestionIndex.INDEX_NAME)
            except NotFoundError:
                pass

        if dm.has_errors:
            errors_body = dm.render_errors_for_store()
            es.index(ErrorIndex.INDEX_NAME, ErrorIndex.TYPE_NAME, body=errors_body, id=dm.id.value)
            es.indices.refresh(index=ErrorIndex.INDEX_NAME)
        else:
            delete_error(dm.id.value)

    if update_inplace:
        dm_body = dm.render_for_store()
        es.update(DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME, id=dm.id.value,
                  body={'doc': dm_body})
        es.indices.refresh(index=DocumentIndex.INDEX_NAME)

    elif dm.storable_values_updated:
        dm_body = dm.render_for_store()
        es.update(DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME, id=dm.id.value,
                  body={'doc': dm_body})
        es.indices.refresh(index=DocumentIndex.INDEX_NAME)

        om_body = om.render_for_store()
        es.index(OldVersionIndex.INDEX_NAME, doc_type=OldVersionIndex.TYPE_NAME, body=om_body)
        es.indices.refresh(index=OldVersionIndex.INDEX_NAME)
    else:
        raise DocumentNotChangedException(dm.id.value, dm.urls.value[0])


@functions.handle_connection_errors
def delete(dm: DocumentModel, old_models: List[DocumentModel]) -> None:
    es.delete(DocumentIndex.INDEX_NAME, id=dm.id.value, doc_type=DocumentIndex.TYPE_NAME)
    es.indices.refresh(index=DocumentIndex.INDEX_NAME)

    if dm.has_suggestions:
        es.delete(SuggestionIndex.INDEX_NAME, id=dm.id.value, doc_type=SuggestionIndex.TYPE_NAME)
        es.indices.refresh(index=SuggestionIndex.INDEX_NAME)

    if dm.has_errors:
        es.delete(ErrorIndex.INDEX_NAME, id=dm.id.value, doc_type=ErrorIndex.TYPE_NAME)
        es.indices.refresh(index=ErrorIndex.INDEX_NAME)

    for old_dm in old_models:
        es.delete(OldVersionIndex.INDEX_NAME, id=old_dm.id.value, doc_type=OldVersionIndex.TYPE_NAME)

    es.indices.refresh(index=OldVersionIndex.INDEX_NAME)


@functions.handle_connection_errors
def store_feed(body: dict):
    es.index(FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME, body=body)


@functions.handle_connection_errors
def update_feed(feed_id, body):
    es.update(FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME, id=feed_id, body={'doc': body})
