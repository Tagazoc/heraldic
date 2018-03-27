#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Document test module.
"""

from src.tests.media.liberation_test import *
from src.models.document import Document
import pytest
from src.rendering.flask.factory import create_app
from src.heraldic_exceptions import DocumentNotFoundException
from src.store.model_searcher import retrieve_errors, retrieve_old_versions, retrieve_suggestions


# Flask test configuration
config = {
    "TESTING": True,
    "WTF_CSRF_ENABLED": False
}
app = create_app(config)
app_client = app.test_client()
url = doc_dict['urls']


def test_url_submit():
    """
    Test URL submission on Web interface within its Web response, then the attributes and suggestions of the document
    retrieved from store. No old version should exist yet.
    """
    rv = app_client.post('/submit_document', data=dict(
        url=url
    ), follow_redirects=True)
    assert "a été récupéré" in str(rv.data, 'utf-8')

    d = Document(url)
    d.retrieve_from_url()
    d.retrieve_old_versions()

    # Prepare next test
    update_doc_dict['id'] = d.model.id.value

    for k, v in doc_dict.items():
        assert (d.model.attributes[k].render_for_display() == v)

    for k, v in suggestion_dict.items():
        assert (d.model.attributes[k].render_suggestions_for_display() == v)

    assert d.old_versions == []


def test_document_update():
    """
    Test document update from Web interface within its Web response, then attributes of the document from store, and
    the old version of the document.
    """
    rv = app_client.post('/review_document', data=update_doc_dict, follow_redirects=True)
    assert "mis à jour" in str(rv.data, 'utf-8')

    d = Document()
    d.retrieve(update_doc_dict['id'])
    d.retrieve_old_versions()

    for k, v in update_result_dict.items():
        assert (d.model.attributes[k].render_for_display() == v)

    for k, v in suggestion_dict.items():
        assert (d.model.attributes[k].render_suggestions_for_display() == v)

    for i in range(0, len(update_old_model_list)):
        for k, v in update_old_model_list[i].items():
            assert (d.old_versions[i].attributes[k].render_for_display() == v)


def test_document_gather_again():
    """
    Test another gathering of this document from Web interface, and its Web response. Suggestions will be the same yet
    refreshed, but document version and attributes will not update.
    """
    update_doc_dict['gather_again'] = 'Récupérer à nouveau'
    rv = app_client.post('/review_document', data=update_doc_dict, follow_redirects=True)
    assert "constaté" in str(rv.data, 'utf-8')

    d = Document()
    d.retrieve(update_doc_dict['id'])
    d.retrieve_old_versions()

    for k, v in update_result_dict.items():
        assert (d.model.attributes[k].render_for_display() == v)

    for k, v in suggestion_dict.items():
        assert (d.model.attributes[k].render_suggestions_for_display() == v)

    for i in range(0, len(update_old_model_list)):
        for k, v in update_old_model_list[i].items():
            assert (d.old_versions[i].attributes[k].render_for_display() == v)


def test_document_error():
    """
    Test malformed document gathering from a slightly different file with parsing error. Event though document will be
    update, rroneous attribute will not change. Error will be stored in specific index.
    """
    d = Document(url)
    d.retrieve(update_doc_dict['id'])
    d.gather(override=True, filepath='src/tests/media/article_liberation.htm')

    del d

    d = Document()
    d.retrieve(update_doc_dict['id'])
    d.retrieve_old_versions()

    for k, v in error_result_dict.items():
        assert (d.model.attributes[k].render_for_display() == v)

    assert (retrieve_suggestions(update_doc_dict['id']) == {})

    for k in errors_list:
        assert (d.model.attributes[k].parsing_error is not None)

    for i in range(0, len(error_old_model_list)):
        for k, v in error_old_model_list[i].items():
            assert (d.old_versions[i].attributes[k].render_for_display() == v)


def test_document_error_solved():
    """
    Gather "again" the document from original URL. No more errors, and document attributes are once again updated to
    "original" values.
    """
    update_doc_dict['gather_again'] = 'Récupérer à nouveau'
    rv = app_client.post('/review_document', data=update_doc_dict, follow_redirects=True)

    assert "de nouveau" in str(rv.data, 'utf-8')

    d = Document()
    d.retrieve(update_doc_dict['id'])
    d.retrieve_old_versions()

    for k, v in final_gather_dict.items():
        assert (d.model.attributes[k].render_for_display() == v)

    for k, v in suggestion_dict.items():
        assert (d.model.attributes[k].render_suggestions_for_display() == v)

    for i in range(0, len(final_old_model_list)):
        for k, v in final_old_model_list[i].items():
            assert (d.old_versions[i].attributes[k].render_for_display() == v)


def test_document_deletion():
    """
    Deletion of the document, and its attached objects : suggestions, errors (should not be) and old versions.
    """
    d = Document(url)
    d.retrieve_from_url()
    d.retrieve_old_versions()
    d.delete()

    with pytest.raises(DocumentNotFoundException):
        d.retrieve(update_doc_dict['id'])

    assert (retrieve_errors(update_doc_dict['id']) == {})

    assert (retrieve_suggestions(update_doc_dict['id']) == {})

    assert (retrieve_old_versions(update_doc_dict['id']) == [])
