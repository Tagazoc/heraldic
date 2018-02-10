#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Document class.
"""

from src.media.known_media import KnownMedia
from src.store import model_storer, model_searcher
from src.gathering.html_document_gatherer import HTMLDocumentGatherer
from src.models.document_model import DocumentModel


class Document(object):
    """
    Class representing a Document during its way through Heraldic.
    """
    def __init__(self):
        self.model = DocumentModel()
        self.old_versions = []

        self.extractor = None

        self.gatherer = None

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
        return model_storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str):
        """
        Retrieve document contents from a store.
        :param doc_id: ID of the document in the store
        """
        self.model = model_searcher.retrieve(doc_id)

    def retrieve_from_url(self, url: str):
        """
        Retrieve a document from its URL.
        :param url: URL of the document
        """
        self.model = model_searcher.retrieve_from_url(url)

    def retrieve_old_versions(self, doc_id: str):
        """
        Retrieve old versions of a document from its ID.
        :param doc_id: ID of the document in the store
        """
        self.old_versions = model_searcher.retrieve_old_versions(doc_id)
        self._set_attributes_versions()

    def update_from_model(self, new_model: DocumentModel):
        """
        Update document from another model, updating model and adding old model (containing old attributes' values)
        to old versions list.
        :param new_model: new model which attributes will override old ones (Cthulu ftaghn)
        :return:
        """
        old_model = self.model.update(new_model)
        self.old_versions.append(old_model)
        model_storer.update(self.model, old_model)

    def update_from_display(self, attribute_dict: dict):
        """
        Update document from display (web form).
        :param attribute_dict: dict with values originating from display
        :return:
        """
        new_model = DocumentModel()
        new_model.set_from_display(attribute_dict)
        self.update_from_model(new_model)

    def _set_attributes_versions(self):
        """
        Set version for each attribute : it is not trivial as only old values are stored in old versions models,
        so the attribute's version does not equal the model's version.
        :return:
        """
        counter_dict = {}
        for model in self.old_versions + [self.model]:
            for (k, v) in model.attributes.items():
                # Take only initialized attributes into account
                if v.initialized:
                    if k not in counter_dict:
                        # Necessary the first version for the first occurrence of k
                        v.version_no = 1
                    else:
                        # Use attribute counter to get the correct version number
                        v.version_no = counter_dict[k]
                    # Next model version will be used as next occurrence of this attribute
                    counter_dict[k] = model.version_no.value + 1

