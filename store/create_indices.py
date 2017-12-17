#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test file
"""
from datetime import datetime
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch
from src.models.document_model import DocumentModel

host = '127.0.0.1:1080'
es = Elasticsearch(host)

ic = IndicesClient(es)

docs_mapping = '''
{
    "mappings": {
        "doc": {
            "properties": {
            '''

model = DocumentModel()
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

ic.create('docs', body=docs_mapping)
ic.create('docs_history', body=docs_mapping)


ic.create('words', body=words_mapping)

