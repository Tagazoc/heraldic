#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module defines Elasticsearch instance, index class and indexes.
"""

from elasticsearch import Elasticsearch
from elasticsearch.client.indices import IndicesClient
from src.models.document_model import DocumentModel, OldDocumentModel
from elasticsearch.exceptions import NotFoundError

ELASTICSEARCH_HOST = {'host': '127.0.0.1', 'port': 1080}
es = Elasticsearch([ELASTICSEARCH_HOST])


class ElasticIndex:
    INDEX_NAME = ''
    TYPE_NAME = ''

    @classmethod
    def render_mapping_body(cls) -> str:
        docs_mapping = '''{
                    "mappings": {
                        "''' + cls.TYPE_NAME + '''": {
                            "properties": {
                            '''
        docs_mapping += cls._render_mapping_body()
        docs_mapping += '''                    }
                }
            }
        }'''
        return docs_mapping

    @classmethod
    def _render_mapping_body(cls) -> str:
        return ""

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
    def _render_mapping_body(cls):
        model = DocumentModel()
        properties_mapping = ''

        for k, v in model.attributes.items():
            if v.storable:
                properties_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
                if v.store_format:
                    properties_mapping += ', "format": "' + v.store_format + '"\n'
                properties_mapping += '},\n'
        # Removing last comma
        properties_mapping = properties_mapping[:-2] + '\n'

        return properties_mapping


class OldVersionIndex(ElasticIndex):
    INDEX_NAME = 'docs_history'
    TYPE_NAME = 'doc'

    @classmethod
    def _render_mapping_body(cls):
        model = OldDocumentModel(1)
        properties_mapping = ''

        for k, v in model.attributes.items():
            if v.storable:
                properties_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
                if v.store_format:
                    properties_mapping += ', "format": "' + v.store_format + '"\n'
                properties_mapping += '},\n'
        # Removing last comma
        properties_mapping = properties_mapping[:-2] + '\n'

        return properties_mapping


class ErrorIndex(ElasticIndex):
    INDEX_NAME = 'errors'
    TYPE_NAME = 'doc_errors'

    @classmethod
    def _render_mapping_body(cls):
        model = DocumentModel()
        properties_mapping = ''

        for k, v in model.attributes.items():
            if v.extractible and v.storable:
                properties_mapping += '"' + k + '": {\n"type": "text"'
                properties_mapping += '},\n'
        # Removing last comma
        properties_mapping = properties_mapping[:-2] + '\n'

        return properties_mapping


class SuggestionIndex(ElasticIndex):
    INDEX_NAME = 'suggestions'
    TYPE_NAME = 'doc'

    @classmethod
    def _render_mapping_body(cls):
        model = DocumentModel()
        properties_mapping = ''
        for k, v in model.attributes.items():
            if v.storable and v.extractible and v.revisable:
                properties_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
                if v.store_format:
                    properties_mapping += ', "format": "' + v.store_format + '"\n'
                properties_mapping += '},\n'
        # Removing last comma
        properties_mapping = properties_mapping[:-2] + '\n'

        return properties_mapping


class FeedsIndex(ElasticIndex):
    INDEX_NAME = 'feeds'
    TYPE_NAME = 'feed'

    @classmethod
    def _render_mapping_body(cls):
        properties_mapping = ''
        attributes = ['url', 'title', 'link']
        for k in attributes:
            properties_mapping += '"' + k + '": {\n"type": "keyword"},\n'
        properties_mapping += '"update_time": {\n"type": "date", "format": "epoch_millis"},\n'
        # Removing last comma
        properties_mapping = properties_mapping[:-2] + '\n'

        return properties_mapping
