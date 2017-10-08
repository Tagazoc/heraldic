#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete indices (beware !)
"""
from datetime import datetime
from elasticsearch.client.indices import IndicesClient
from elasticsearch import Elasticsearch
es = Elasticsearch()

ic = IndicesClient(es)

ic.delete('docs')

ic.delete('words')

