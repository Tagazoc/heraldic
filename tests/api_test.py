#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Document test module.
"""

from tests.medias.liberation_test import *
from heraldic.models.document import Document
import pytest
import requests
import heraldic.misc.exceptions as ex
from heraldic.store.index_searcher import retrieve_errors, retrieve_suggestions, retrieve_old_version_models
import json

api_url = 'http://localhost:5000/api/'
doc_id = ''


@pytest.fixture(scope="session", autouse=True)
def delete_test_doc():
    # Deletion if document exists without API as it is not available in API
    d = Document(url)
    d.retrieve_old_versions()
    try:
        d.delete()
    except ex.DeletionError:
        pass


def test_media():
    """
    Test media API calls
    :return:
    """
    response = requests.get(api_url + 'media/' + media_id)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    json_data = json.loads(response.text)

    assert json_data['id'] == media_id
    assert json_data['name'] == media_name
    assert isinstance(json_data['count'], int) and json_data['count'] > 0


def test_search_url_not_found():
    """
    Test search for an URL which does not exist in store.
    :return:
    """
    response = requests.get(api_url + 'docs', params=dict(
        url=url
    ))
    assert response.status_code == 404


def test_url_submit():
    """
    Test URL submission on API, then the attributes of the document
    retrieved from API. No old version should exist yet.
    """
    global doc_id
    response = requests.post(api_url + 'docs', data=dict(
        url=url
    ))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc_id = json.loads(response.text)

    assert isinstance(doc_id, str)

    response = requests.get(api_url + 'docs/' + doc_id)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc = json.loads(response.text)
    for k, v in doc_dict.items():
        # Arrays in elastic are unordered
        if isinstance(v, list):
            assert set(doc['model'][k]) == set(v)
        else:
            assert doc['model'][k] == v


def test_search_url():
    """
    Test search for the URL which just has been submitted.
    :return:
    """
    response = requests.get(api_url + 'docs', params=dict(
        url=url
    ))
    assert response.status_code == 200
    doc = json.loads(response.text)
    assert doc['model']['id'] == doc_id


def test_bad_domain_url_submit():
    """
    Test URL submission on API with a domain which is not supported.
    :return:
    """
    response = requests.post(api_url + 'docs', data=dict(
        url=bad_domain_url
    ))
    assert response.status_code == 501


def test_document_update():
    """
    Test document update from a file, then compare attributes of the document retrieved with API, and
    the old version of the document.
    """
    update_d = Document(url, filepath=article_filepath_update)
    update_d.gather()

    response = requests.get(api_url + 'docs/' + doc_id + '?with_history=true')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc = json.loads(response.text)
    for k, v in update_doc_dict.items():
        # Arrays in elastic are unordered
        if isinstance(v, list):
            assert set(doc['model'][k]) == set(v)
        else:
            assert doc['model'][k] == v

    assert doc['errors'] == {}
    doc_versions = doc['versions']
    for doc_version, update_doc_version in zip(doc_versions, update_doc_versions):
        for (k, v) in update_doc_version.items():
            # Arrays in elastic are unordered
            if isinstance(v, list):
                assert set(doc_version[k]) == set(v)
            else:
                assert doc_version[k] == v


def test_document_error():
    """
    Test malformed document gathering from a slightly different file with parsing error. Even though document will be
    updated, erroneous attribute will not change. Error will be stored in specific index.
    """
    d = Document(url, filepath=article_filepath_error)
    d.gather()

    del d

    response = requests.get(api_url + 'docs/' + doc_id + '?with_history=true')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc = json.loads(response.text)

    for k, v in error_doc_dict.items():
        # Arrays in elastic are unordered
        if isinstance(v, list):
            assert set(doc['model'][k]) == set(v)
        else:
            assert doc['model'][k] == v

    for k, v in error_doc_errors.items():
        assert doc['errors'][k] == v
        # Assert there is no error left
        del doc['errors'][k]
    assert doc['errors'] == {}

    doc_versions = doc['versions']
    for doc_version, error_doc_version in zip(doc_versions, error_doc_versions):
        for (k, v) in error_doc_version.items():
            # Arrays in elastic are unordered
            if isinstance(v, list):
                assert set(doc_version[k]) == set(v)
            else:
                assert doc_version[k] == v


def test_document_error_solved():
    """
    Gather the document without parsing error. Error is now deleted.
    """
    d = Document(url, filepath=article_filepath_error_solved)
    d.gather()

    del d

    response = requests.get(api_url + 'docs/' + doc_id + '?with_history=true')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc = json.loads(response.text)

    for k, v in error_solved_doc_dict.items():
        # Arrays in elastic are unordered
        if isinstance(v, list):
            assert set(doc['model'][k]) == set(v)
        else:
            assert doc['model'][k] == v

    assert doc['errors'] == {}

    doc_versions = doc['versions']
    for doc_version, error_solved_doc_version in zip(doc_versions, error_solved_doc_versions):
        for (k, v) in error_solved_doc_version.items():
            # Arrays in elastic are unordered
            if isinstance(v, list):
                assert set(doc_version[k]) == set(v)
            else:
                assert doc_version[k] == v


def test_document_update_inplace():
    """
    Gather the original document with "inplace" flag, in order to enhance parser for example. Only the last version
    of the document should be updated.
    """
    d = Document(url)
    d.gather(update_inplace=True)

    del d

    response = requests.get(api_url + 'docs/' + doc_id + '?with_history=true')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    doc = json.loads(response.text)

    for k, v in update_inplace_doc_dict.items():
        # Arrays in elastic are unordered
        if isinstance(v, list):
            assert set(doc['model'][k]) == set(v)
        else:
            assert doc['model'][k] == v

    assert doc['errors'] == {}

    doc_versions = doc['versions']
    for doc_version, update_inplace_doc_version in zip(doc_versions, update_inplace_doc_versions):
        for (k, v) in update_inplace_doc_version.items():
            # Arrays in elastic are unordered
            if isinstance(v, list):
                assert set(doc_version[k]) == set(v)
            else:
                assert doc_version[k] == v


def test_document_deletion():
    """
    Deletion of the document, and its attached objects : suggestions, errors (should not be) and old versions.
    """
    d = Document(url)
    d.retrieve_old_versions()
    d.delete()

    response = requests.get(api_url + 'docs/' + doc_id + '?with_history=true')
    assert response.status_code == 404

    assert (retrieve_errors(doc_id) == {})

    assert (retrieve_suggestions(doc_id) == {})

    assert (list(retrieve_old_version_models(doc_id)) == [])
