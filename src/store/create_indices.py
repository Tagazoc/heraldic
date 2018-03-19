#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test file
"""
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch
from src.models.document_model import DocumentModel, OldDocumentModel

host = '127.0.0.1:1080'
es = Elasticsearch(host)

ic = IndicesClient(es)

model = DocumentModel()

docs_mapping = '''
{
    "mappings": {
        "doc": {
            "properties": {
            '''


for k, v in model.attributes.items():
    if v.storable:
        docs_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
        if v.store_format:
            docs_mapping += ', "format": "' + v.store_format + '"\n'
        docs_mapping += '},\n'

docs_mapping += '''                
                "words": {
                    "type": "nested"
                }
            }
        }
    }
}'''

old_model = OldDocumentModel('1')
docs_history_mapping = '''
{
    "mappings": {
        "doc": {
            "properties": {
            '''
for k, v in old_model.attributes.items():
    if v.storable:
        docs_history_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
        if v.store_format:
            docs_history_mapping += ', "format": "' + v.store_format + '"\n'
        docs_history_mapping += '},\n'

docs_history_mapping += '''                
                "words": {
                    "type": "nested"
                }
            }
        }
    }
}'''


words_mapping = '''
{  
    "mappings": {  
        "word": {
            "properties": {
                "expression": {
                    "type": "keyword"
                },
                "pos": {  
                    "type": "keyword"
                },
                "docs": {
                    "type": "keyword"
                }
            }
        }
    }
}'''

errors_mapping = '''
{
    "mappings": {
        "doc_errors": {
            "properties": {
            '''


for k, v in model.attributes.items():
    if v.extractible and v.storable:
        errors_mapping += '"' + k + '": {\n"type": "text"'
        errors_mapping += '},\n'
# Removing last comma
errors_mapping = errors_mapping[:-2] + '\n'

errors_mapping += '''
            }
        }
    }
}'''

suggestions_mapping = '''
{
    "mappings": {
        "doc": {
            "properties": {
            '''


for k, v in model.attributes.items():
    if v.storable and v.extractible and v.revisable:
        suggestions_mapping += '"' + k + '": {\n"type": "' + v.storable + '"'
        if v.store_format:
            suggestions_mapping += ', "format": "' + v.store_format + '"\n'
        suggestions_mapping += '},\n'
# Removing last comma
suggestions_mapping = suggestions_mapping[:-2] + '\n'
suggestions_mapping += '''
            }
        }
    }
}'''


ic.create('errors', body=errors_mapping)
ic.create('suggestions', body=suggestions_mapping)
ic.create('docs', body=docs_mapping)
ic.create('docs_history', body=docs_history_mapping)


ic.create('words', body=words_mapping)
