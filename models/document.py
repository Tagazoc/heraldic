#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Document class.
"""

from src.media.known_media import KnownMedia
from src.store.document_storer import DocumentStorer
from src.gathering.html_document_gatherer import HTMLDocumentGatherer
from src.models.document_model import DocumentModel
from elasticsearch import Elasticsearch


class Document(object):
    """
    Class representing a Document during its way through Heraldic.
    """
    def __init__(self, es: Elasticsearch):
        self.model = DocumentModel()
        self.old_versions = []

        self.extractor = None

        self.storer = DocumentStorer(es)

        self.gatherer = None
        self.renderer = None

    def gather(self, url: str):
        """
        Gather a document contents from an url.
        :param url: URL of the document
        :return:
        """
        if not self.gatherer:
            self.gatherer = HTMLDocumentGatherer(self.model, url)
        self.gatherer.gather()

    def extract_fields(self):
        """
        Find document media and extract document fields according to it.
        :return:
        """
        if not self.extractor:
            extractor = KnownMedia()[self.model.domain]
            self.extractor = extractor(self.model)
        self.extractor.extract_fields()

    def store(self, doc_id: str=None):
        """
        Store document contents.
        :param doc_id: ID of the document in the store
        :return:
        """
        return self.storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str):
        """
        Retrieve document contents from a store.
        :param doc_id: ID of the document in the store
        :return:
        """
        self.model = self.storer.retrieve(doc_id)

    def retrieve_from_url(self, url: str):
        self.model = self.storer.retrieve_from_url(url)

    def update_from_display(self, attribute_dict: dict):
        """
        Update document from display (web form), updating model and adding old model (containing old attributes' values)
        to old versions list.
        :param attribute_dict: dict with values originating from display
        :return:
        """
        new_model = DocumentModel()
        new_model.set_from_display(attribute_dict)
        old_model = self.model.update(new_model)
        self.old_versions.append(old_model)
        self.storer.update(self.model, old_model)

