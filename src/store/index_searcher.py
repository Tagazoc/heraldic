#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing index search functions.
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
    hits = _search_query({'match': {'urls': url}}, terminate_after=1, _source=False)
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
    hits = _search_query(query, terminate_after=1, _source=False)

    return len(hits) > 0


def search(q=None, body_query=None, limit: int=0) -> List[DocumentModel]:
    from_ = 0
    total_hits = []
    size = 100

    hits = _search_query(query=body_query, q=q, from_=from_, size=size, terminate_after=limit)
    total_hits.extend(hits['hits'])
    from_ += size
    while hits['total'] > from_:
        hits = _search_query(query=body_query, q=q, from_=from_, size=size, terminate_after=limit)
        total_hits.extend(hits['hits'])
        from_ += size

    return _generate_doc_models(total_hits)


def count(q=None, body_query=None, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME) -> int:
    return es.count(index=index, doc_type=doc_type, q=q, body=body_query)


def search_all_errors() -> List[dict]:
    res = _search_query({}, ErrorIndex.INDEX_NAME, ErrorIndex.TYPE_NAME)


def search_url(url) -> List[DocumentModel]:
    hits = _search_query({'match': {'urls': url}}, terminate_after=1)
    return _generate_doc_models(hits['hits'])


def retrieve_old_versions(doc_id) -> List[DocumentModel]:
    models = []
    hits = _search_query({'term': {'doc_id': doc_id}}, index=OldVersionIndex.INDEX_NAME, sort=['version_no'])

    for hit in hits['hits']:
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
    hits = _search_query(index=FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME)

    return hits['hits']


def _generate_doc_models(hits) -> List[DocumentModel]:
    models = []
    for hit in hits:
        dm = DocumentModel()

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


def _search_query(query: dict=None, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME,
                  **kwargs) -> dict:
    body = {}
    if query is not None:
        body = {'query': query}
    res = es.search(index, doc_type=doc_type, body=body, **kwargs)
    es.search()

    return res['hits']
