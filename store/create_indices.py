#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test file
"""
from datetime import datetime
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch

host = '192.168.1.31:9200'
es = Elasticsearch(host)

ic = IndicesClient(es)

docs_mapping = '''
{
    "mappings": {
        "doc": {
            "properties": {
                "title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "url": {
                    "type": "text"
                },
                "media": {
                    "type": "keyword"
                },
                "gather_timestamp": {
                    "type": "date",
                    "format": "epoch_millis"
                },
                "update_timestamp": {
                    "type": "date",
                    "format": "epoch_millis"                
                },
                "doc_publication_timestamp": {
                    "type": "date",
                    "format": "epoch_millis"                
                },
                "doc_update_timestamp": {
                    "type": "date",
                    "format": "epoch_millis"                
                },
                "category": {
                    "type": "keyword"
                },
                "quotes": {
                    "type": "text"
                },
                "href_sources": {
                    "type": "text"
                },
                "explicit_sources": {
                    "type": "text"
                },                
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

ic.create('words', body=words_mapping)

