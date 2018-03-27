#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing model search functions.
"""

from src.store.elastic import es, DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
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
        res = es.get(DocumentIndex.INDEX_NAME, id=doc_id, doc_type=DocumentIndex.TYPE_NAME)
    except NotFoundError:
        raise DocumentNotFoundException
    dm = DocumentModel()

    dm.id.value = doc_id
    dm.set_from_store(res['_source'])

    dm.set_errors_from_store(retrieve_errors(doc_id))

    dm.set_suggestions_from_store(retrieve_suggestions(doc_id))

    return dm


def check_url_existence(url: str) -> bool:
    """
    Check whether a document exists with this URL.
    :param url: URL of the potential document
    :return: True if a document with this url exists in 'docs' index, else False
    """
    hits = _search_term({'match': {'urls': url}}, limit=1, _source=False)
    return len(hits) > 0


def check_url_uptodate(url: str, update_time) -> bool:
    query = {
        'match': {'urls': url},
        'range': {
            'update_time': {
                "gte": update_time
            }
        }
    }
    hits = _search_term(query, limit=1, _source=False)

    return len(hits) > 0


def search_all_docs() -> List[DocumentModel]:
    return _generate_doc_models(_search_term())


def search_all_errors() -> List[dict]:
    res = _search_term({}, ErrorIndex.INDEX_NAME, ErrorIndex.TYPE_NAME)


def search_url(url) -> List[DocumentModel]:
    return _generate_doc_models(_search_term({'match': {'urls': url}}, limit=1))


def retrieve_old_versions(doc_id) -> List[DocumentModel]:
    models = []
    hits = _search_term({'term': {'doc_id': doc_id}}, index=OldVersionIndex.INDEX_NAME, sort=['version_no'])

    for hit in hits:
        dm = OldDocumentModel(doc_id)

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


def retrieve_errors(doc_id) -> dict:
    try:
        res = es.get(ErrorIndex.INDEX_NAME, id=doc_id, doc_type=ErrorIndex.TYPE_NAME)
        return res['_source']
    except NotFoundError:
        return {}


def retrieve_suggestions(doc_id) -> dict:
    try:
        res = es.get(SuggestionIndex.INDEX_NAME, id=doc_id, doc_type=SuggestionIndex.TYPE_NAME)
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


def retrieve_feeds_dicts() -> List[dict]:
    hits = _search_term(index=FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME)

    return hits


def _generate_doc_models(hits) -> List[DocumentModel]:
    models = []
    for hit in hits:
        dm = DocumentModel()

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


def _search_term(query: dict= {}, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME,
                 limit=0, **kwargs) -> List[dict]:
    body = {}
    if query:
        body = {'query': query}
    if limit:
        body['terminate_after'] = limit
    for k, v in kwargs.items():
        body[k] = v

    res = es.search(index, doc_type=doc_type, body=body)

    return res['hits']['hits']
