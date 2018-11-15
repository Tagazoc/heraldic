#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing index search functions.
"""

from heraldic.store.elastic import es, DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
import heraldic.misc.exceptions as ex
from elasticsearch.exceptions import NotFoundError
from heraldic.models.document_model import DocumentModel, OldDocumentModel
from typing import List, Generator
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


def retrieve_old_version_models(doc_id: str) -> Generator[OldDocumentModel, None, None]:
    for hit in _retrieve_old_versions(doc_id):
        dm = OldDocumentModel(doc_id)

        dm.id.value = hit['_id']
        dm.set_from_store(hit)
        yield dm


def retrieve_all_urls() -> Generator[str, None, None]:
    results = elasticsearch.helpers.scan(es, index=DocumentIndex.INDEX_NAME, doc_type=DocumentIndex.TYPE_NAME,
                                         _source=['urls'])
    for result in results:
        if 'urls' in result['_source'].keys():
            yield result['_source']['urls'][0]


def search_by_media(media_id: str, limit: int=100) -> Generator[DocumentModel, None, None]:
    return _generate_doc_models(_search_query(q="media:" + media_id, limit=limit))


def search_models(q=None, body_query=None, limit: int=0) -> Generator[DocumentModel, None, None]:
    return _generate_doc_models(_search_query(q=q, body_query=body_query, limit=limit))


def search_model_by_url(url: str) -> DocumentModel:
    hits = _search_query({'match': {'urls': url}}, terminate_after=1)
    for hit in _generate_doc_models(hits):
        return hit
    raise ex.DocumentNotFoundException


def search_error_id_by_url(url: str) -> str:
    hits = _search_query({'match': {'urls': url}}, index_class=ErrorIndex,
                         terminate_after=1)
    # Return first element's id, if no element return None
    try:
        hit = next(hits)
        return hit['_id']
    except StopIteration:
        return None


def retrieve_error_url(doc_id: str) -> str:
    try:
        res = es.get(ErrorIndex.INDEX_NAME, id=doc_id, doc_type=ErrorIndex.TYPE_NAME)
    except NotFoundError:
        raise ex.DocumentNotFoundException

    return res['_source']['urls'][0]


def get_similar_errors_urls(error_body: str, media: str) -> Generator[str, None, None]:
    query = {
        'bool': {
            'must': [{
                'term': {
                    'body.keyword': error_body
                }
            }, {
                'term': {
                    'media': media
                }
            }]
        }
    }
    hits = _search_query(query, index_class=ErrorIndex, sort='gather_time:desc')
    for hit in hits:
        yield hit['_source']['urls'][0]


def _generate_doc_models(hits) -> Generator[DocumentModel, None, None]:
    for hit in hits:
        dm = DocumentModel()

        dm.id.value = hit['_id']
        dm.set_from_store(hit['_source'])
        yield dm


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
    try:
        next(hits)
        return True
    except StopIteration:
        return False


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
    try:
        next(hits)
        return True
    except StopIteration:
        return False


@handle_connection_errors
def count(q=None, body_query=None, index_class=DocumentIndex) -> int:
    return es.count(index=index_class.INDEX_NAME, doc_type=index_class.TYPE_NAME, q=q, body=body_query)['count']


def _retrieve_old_versions(doc_id) -> Generator[dict, None, None]:
    hits = _search_query({'term': {'doc_id': doc_id}}, index_class=OldVersionIndex, sort=['version_no'])

    for hit in hits:
        hit['_source']['_id'] = hit['_id']
        yield hit['_source']


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


@handle_connection_errors
def retrieve_feeds_dicts(media_id=None) -> List[dict]:
    query = {'match': {'media_id': media_id}} if media_id else None
    hits = _search_query(query=query, index_class=FeedsIndex)

    return hits


@handle_connection_errors
def _search_query(query: dict=None, index_class=DocumentIndex, **kwargs) -> Generator[dict, None, None]:
    body = {}
    if query is not None:
        body = {'query': query}
    results = elasticsearch.helpers.scan(es, query=body, index=index_class.INDEX_NAME, doc_type=index_class.TYPE_NAME,
                                         **kwargs)
    return results
