#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing model search functions.
"""

from src.store.elastic import es
from src.models.document_model import DocumentModel, OldDocumentModel
from src.heraldic_exceptions import DocumentNotFoundException
from elasticsearch.exceptions import NotFoundError
from typing import List


def retrieve(doc_id: str) -> DocumentModel:
    """
    Retrieve document from store.
    :param doc_id: ID of the document
    :return: The document model.
    """
    try:
        res = es.get('docs', id=doc_id, doc_type='doc')
    except NotFoundError:
        raise DocumentNotFoundException
    dm = DocumentModel()

    dm.id.value = doc_id
    dm.set_from_store(res['_source'])

    dm.set_errors_from_store(retrieve_errors(doc_id))

    dm.set_suggestions_from_store(retrieve_suggestions(doc_id))

    return dm


def search_all_docs() -> List[DocumentModel]:
    return _generate_doc_models(_search_term())


def search_url(url) -> List[DocumentModel]:
    return _generate_doc_models(_search_term({'url': url}, limit=1))


def retrieve_old_versions(doc_id) -> List[DocumentModel]:
    models = []
    hits = _search_term({'doc_id': doc_id}, index='docs_history', sort=['version_no'])

    for hit in hits:
        dm = OldDocumentModel(doc_id)

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


def retrieve_errors(doc_id) -> dict:
    try:
        res = es.get('errors', id=doc_id, doc_type='doc_errors')
        return res['_source']
    except NotFoundError:
        return {}


def retrieve_suggestions(doc_id) -> dict:
    try:
        res = es.get('suggestions', id=doc_id, doc_type='doc')
        return res['_source']
    except NotFoundError:
        return {}


def retrieve_from_url(url: str) -> DocumentModel:
    hits = search_url(url)
    try:
        dm = hits[0]
    except IndexError:
        raise DocumentNotFoundException

    dm.set_errors_from_store(retrieve_errors(dm.id.value))

    dm.set_suggestions_from_store(retrieve_suggestions(dm.id.value))

    return dm


def _generate_doc_models(hits) -> List[DocumentModel]:
    models = []
    for hit in hits:
        dm = DocumentModel()

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


def _search_term(terms: dict= {}, index='docs', limit=0, sort: list= None) -> List[DocumentModel]:
    body = {}
    if terms:
        body = {'query': {'term': terms}}
    if limit:
        body['terminate_after'] = limit
        pass
    if sort:
        body['sort'] = sort

    res = es.search(index, 'doc', body)

    return res['hits']['hits']
