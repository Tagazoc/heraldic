#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete indices (beware !)
"""
from datetime import datetime
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch

host = '127.0.0.1:1080'
es = Elasticsearch(host)

ic = IndicesClient(es)

ic.delete('docs')

ic.delete('words')

