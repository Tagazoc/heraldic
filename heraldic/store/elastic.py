#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module defines Elasticsearch instance, index class and indexes.
"""

from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient
from heraldic.models.document_model import DocumentModel, OldDocumentModel
from elasticsearch.exceptions import NotFoundError

ELASTICSEARCH_HOST = {'host': '127.0.0.1', 'port': 1080}
es = Elasticsearch([ELASTICSEARCH_HOST])


class ElasticIndex:
    INDEX_NAME = ''
    TYPE_NAME = ''

    @classmethod
    def render_mapping_body(cls) -> dict:
        docs_mapping = {
            'mappings': {
                cls.TYPE_NAME: {
                    "properties": cls._render_mapping_body()
                }
            }
        }
        return docs_mapping

    @classmethod
    def _render_mapping_body(cls) -> dict:
        return {}

    @classmethod
    def create(cls):
        ic = IndicesClient(es)
        ic.create(cls.INDEX_NAME, body=cls.render_mapping_body())

    @classmethod
    def delete(cls):
        ic = IndicesClient(es)
        try:
            ic.delete(cls.INDEX_NAME)
        except NotFoundError:
            pass


class DocumentIndex(ElasticIndex):
    INDEX_NAME = 'docs'
    TYPE_NAME = 'doc'

    @classmethod
    def _render_mapping_body(cls) -> dict:
        model = DocumentModel()
        return {k: v.storable for k, v in model.attributes.items() if v.storable}


class OldVersionIndex(ElasticIndex):
    INDEX_NAME = 'docs_history'
    TYPE_NAME = 'doc'

    @classmethod
    def _render_mapping_body(cls):
        model = OldDocumentModel(doc_id=1)
        return {k: v.storable for k, v in model.attributes.items() if v.storable}


class ErrorIndex(ElasticIndex):
    INDEX_NAME = 'errors'
    TYPE_NAME = 'doc_errors'

    @classmethod
    def _render_mapping_body(cls):
        model = DocumentModel()
        body = {k: {'type': 'text'} for k, v in model.attributes.items() if v.storable and v.extractible
                or k == 'urls'}
        body['gather_time'] = {'type': 'date', 'format': 'epoch_millis'}
        body['media'] = {'type': 'keyword'}
        body['urls'] = {'type': 'keyword'}
        return body


class SuggestionIndex(ElasticIndex):
    INDEX_NAME = 'suggestions'
    TYPE_NAME = 'doc'

    @classmethod
    def _render_mapping_body(cls):
        model = DocumentModel()
        return {k: v.storable for k, v in model.attributes.items() if v.storable and v.extractible and v.revisable}


class FeedsIndex(ElasticIndex):
    INDEX_NAME = 'feeds'
    TYPE_NAME = 'feed'

    @classmethod
    def _render_mapping_body(cls):
        return {
            'url': {'type': 'keyword'},
            'title': {'type': 'keyword'},
            'link': {'type': 'keyword'},
            'update_time': {'type': 'date', 'format': 'epoch_millis'}
        }
