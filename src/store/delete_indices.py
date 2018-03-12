#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete indices (beware !)
"""
from datetime import datetime
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

host = '127.0.0.1:1080'
es = Elasticsearch(host)

ic = IndicesClient(es)

try:
    ic.delete('docs')
except NotFoundError:
    pass
try:
    ic.delete('docs_history')
except NotFoundError:
    pass
try:
    ic.delete('words')
except NotFoundError:
    pass
try:
    ic.delete('errors')
except NotFoundError:
    pass
try:
    ic.delete('suggestions')
except NotFoundError:
    pass
