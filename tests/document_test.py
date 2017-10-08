#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Document test module.
"""

from src.tests.media.lemonde_test import *

from elasticsearch import Elasticsearch
from src.models.document import DocumentModel, Document
import pytest

d = Document()
doc_id = 'UWiHsnxpzZry7bc'
host = '192.168.1.31:9200'
gather_date = None
update_date = None


def test_document_gathering():
    d.gather(url)
    assert (d.model.content.startswith(response_beginning))


def test_document_extract():
    d.extract_fields()

    # Print everything to build test vars
    print('title = "' + d.model.title.replace('"', '\\"') + '"')
    print('description = "' + d.model.description.replace('"', '\\"') + '"')
    print('category = "' + d.model.category.replace('"', '\\"') + '"')
    print('quotes = ' + d.model.quotes.__str__())
    print('body = "' + d.model.body.replace('"', '\\"') + '"')
    print('href_sources = ' + d.model.href_sources.__str__())
    print('explicit_sources = ' + d.model.explicit_sources.__str__())

    assert (d.model.title == title)
    assert (d.model.description == description)
    assert (d.model.category == category)
    assert (d.model.quotes == quotes)
    assert (d.model.href_sources == href_sources)
    assert (d.model.explicit_sources == explicit_sources)


@pytest.mark.skip(reason="No Elastic yet")
def test_document_store():
    global doc_id
    doc_id = d.model.media_name + doc_id

    res = d.store(doc_id, host)
    assert res

    es = Elasticsearch(host)

    res = es.get('docs', doc_id)
    assert (res['_source']['title'] == title)
    assert (res['_source']['description'] == description)
    assert (res['_source']['category'] == category)
    assert (res['_source']['quotes'] == quotes)
    assert (res['_source']['href_sources'] == href_sources)
    assert (res['_source']['explicit_sources'] == explicit_sources)

    res = es.delete('docs', 'doc', doc_id)
    assert (res['result'] == 'deleted')


@pytest.mark.skip(reason="No Elastic yet")
def test_document_retrieve():
    d.retrieve(doc_id, host)
    assert isinstance(d.model, DocumentModel)

    assert (d.model.title == title)
    assert (d.model.description == description)
    assert (d.model.category == category)
    assert (d.model.quotes == quotes)
    assert (d.model.href_sources == href_sources)
    assert (d.model.explicit_sources == explicit_sources)

    assert ()
