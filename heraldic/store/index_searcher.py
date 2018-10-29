#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing index search functions.
"""

from heraldic.store.elastic import es, DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
import heraldic.misc.exceptions as ex
from elasticsearch.exceptions import NotFoundError
from heraldic.models.document_model import DocumentModel, OldDocumentModel
from typing import List
import elasticsearch.helpers


def handle_connection_errors(decorated):
    def wrapper(*args, **kwargs):
        try:
            result = decorated(*args, **kwargs)
        except ConnectionError as err:
            raise ex.IndexerConnectionError from err
        return result

    return wrapper


def retrieve_model(doc_id: str) -> DocumentModel:
    """
    Retrieve document from store.
    :param doc_id: ID of the document
    :return: The document model.
    """

    dm = DocumentModel()

    dm.id.value = doc_id
    dm.set_from_store(_retrieve_doc(doc_id))

    dm.set_errors_from_store(retrieve_errors(doc_id))

    dm.set_suggestions_from_store(retrieve_suggestions(doc_id))

    return dm


def retrieve_model_from_url(url: str) -> DocumentModel:
    dm = search_model_by_url(url)

    dm.set_errors_from_store(retrieve_errors(dm.id.value))

    dm.set_suggestions_from_store(retrieve_suggestions(dm.id.value))

    return dm


def retrieve_old_version_models(doc_id: str) -> List[OldDocumentModel]:
    models = []
    for hit in _retrieve_old_versions(doc_id):
        dm = OldDocumentModel(doc_id)

        dm.id.value = hit['_id']
        dm.set_from_store(hit)
        models.append(dm)
    return models


def retrieve_all_urls() -> List[str]:
    results = elasticsearch.helpers.scan(es, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME, _source=['urls'])
    return [hit['_source']['urls'][0] for hit in results if 'urls' in hit['_source'].keys()]


def search_by_media(media_id: str, limit: int=100):
    return _generate_doc_models(_search_docs(q="media:" + media_id, limit=limit))


def search_models(q=None, body_query=None, limit: int=0) -> List[DocumentModel]:
    return _generate_doc_models(_search_docs(q=q, body_query=body_query, limit=limit))


def search_model_by_url(url: str) -> DocumentModel:
    hits = _search_query({'match': {'urls': url}}, terminate_after=1)
    try:
        return _generate_doc_models(hits['hits'])[0]
    except IndexError:
        raise ex.DocumentNotFoundException


def search_error_id_by_url(url: str) -> str:
    hits = _search_query({'match': {'urls': url}}, index=ErrorIndex.INDEX_NAME, doc_type=ErrorIndex.TYPE_NAME,
                         terminate_after=1)
    return hits['hits'][0]['_id'] if hits['hits'] else None


def retrieve_error_url(doc_id: str) -> str:
    try:
        res = es.get(ErrorIndex.INDEX_NAME, id=doc_id, doc_type=ErrorIndex.TYPE_NAME)
    except NotFoundError:
        raise ex.DocumentNotFoundException

    return res['_source']['urls'][0]


def _generate_doc_models(hits) -> List[DocumentModel]:
    models = []
    for hit in hits:
        dm = DocumentModel()

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        models.append(dm)
    return models


@handle_connection_errors
def _retrieve_doc(doc_id: str) -> dict:
    """
    Retrieve document from store.
    :param doc_id: ID of the document
    :return: The document model.
    """
    try:
        res = es.get(DocumentIndex.INDEX_NAME, id=doc_id, doc_type=DocumentIndex.TYPE_NAME)
    except NotFoundError:
        raise ex.DocumentNotFoundException

    return res['_source']


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


def _search_docs(q=None, body_query=None, limit: int=0) -> List:
    hits = elasticsearch.helpers.scan(es, query=body_query, q=q, terminate_after=limit)
    return hits


@handle_connection_errors
def count(q=None, body_query=None, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME) -> int:
    return es.count(index=index, doc_type=doc_type, q=q, body=body_query)['count']


def _retrieve_old_versions(doc_id) -> List:
    hits = _search_query({'term': {'doc_id': doc_id}}, index=OldVersionIndex.INDEX_NAME, sort=['version_no'])

    for hit in hits['hits']:
        hit['_source']['_id'] = hit['_id']

    return [hit['_source'] for hit in hits['hits']]


@handle_connection_errors
def retrieve_errors(doc_id) -> dict:
    try:
        res = es.get(ErrorIndex.INDEX_NAME, id=doc_id, doc_type=ErrorIndex.TYPE_NAME)
        return res['_source']
    except NotFoundError:
        return {}


@handle_connection_errors
def retrieve_suggestions(doc_id) -> dict:
    try:
        res = es.get(SuggestionIndex.INDEX_NAME, id=doc_id, doc_type=SuggestionIndex.TYPE_NAME)
        return res['_source']
    except NotFoundError:
        return {}


def retrieve_feeds_dicts() -> List[dict]:
    hits = _search_query(index=FeedsIndex.INDEX_NAME, doc_type=FeedsIndex.TYPE_NAME, size=1000)

    return hits['hits']


@handle_connection_errors
def _search_query(query: dict=None, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME,
                  **kwargs) -> dict:
    body = {}
    if query is not None:
        body = {'query': query}
    res = es.search(index, doc_type=doc_type, body=body, **kwargs)

    return res['hits']
