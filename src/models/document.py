#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Document class.
"""

from src.media.known_media import known_media
from src.store import index_storer, index_searcher
from src.models.document_model import DocumentModel
from typing import List
from src.misc.exceptions import DocumentExistsException
from src.misc.logging import logger
from src.misc.functions import get_domain
import validators
import re


class Document(object):
    """
    Class representing a Document through its way through Heraldic.
    """
    def __init__(self, url: str=''):
        self.model: DocumentModel = DocumentModel()
        self.old_versions: List[DocumentModel] = []
        self.url = ''
        if url:
            self.url = self._check_and_truncate_url(url)
        # TODO Mettre id ou url ici, avec le retrieve directement

        self.extractor = None

    @classmethod
    def from_model(cls, model):
        doc = cls()
        doc.model = model
        doc.url = model.urls.value[0]
        return doc

    def gather(self, update_time=None, override: bool=False, filepath: str=''):
        """
        Gather a document contents from an url, parse it and store or update it.
        :param update_time: Update time (in rss feed) to avoid gathering if up-to-date
        :param override: disable existence check, in order to override document
        :param filepath: Whether url is instead a file path.
        :return:
        """

        if self.model.urls.value:
            # It is an update, is it already up-to-date ? Unless override flag
            if not override and update_time and self._is_uptodate(update_time):
                raise DocumentExistsException(self.url)
            up_d = Document(self.url)
            if filepath:
                up_d.model.gather_from_file(self.url, filepath)
            else:
                final_url = up_d.model.gather_from_url(self.url)
                self.model.urls.append(self._check_and_truncate_url(final_url))
            up_d._extract_fields()
            self.update_from_model(up_d.model)
            logger.log('INFO_DOC_UPDATE_SUCCESS', self.url)
        else:
            if filepath:
                self.model.gather_from_file(self.url, filepath)
            else:
                final_url = self.model.gather_from_url(self.url)
                self.model.urls.append(self._check_and_truncate_url(final_url))

            self._extract_fields()
            self.store()
            logger.log('INFO_DOC_STORE_SUCCESS', self.url)

    def _extract_fields(self):
        """
        Find document media and extract document fields according to it.
        :return:
        """
        if not self.extractor:
            extractor = known_media.get_media_by_domain(get_domain(self.url))
            self.extractor = extractor(self.model)
        self.extractor.extract_fields()

    def store(self, doc_id: str=None):
        """
        Store document contents.
        :param doc_id: ID of the document in the store
        :return:
        """
        self.model.id = index_storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str):
        """
        Retrieve document contents from a store.
        :param doc_id: ID of the document in the store
        """
        self.model = index_searcher.retrieve(doc_id)
        self.url = self.model.urls.value[0]

    def retrieve_from_url(self):
        """
        Retrieve a document from its URL.
        """
        self.model = index_searcher.retrieve_from_url(self.url)

    def retrieve_old_versions(self):
        """
        Retrieve old versions of a document from its ID.
        """
        self.old_versions = index_searcher.retrieve_old_versions(self.model.id.value)
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
        index_storer.update(self.model, old_model)

    def update_from_revision(self, attribute_dict: dict):
        """
        Update document from display (web form).
        :param attribute_dict: dict with values originating from display
        :return:
        """
        new_model = DocumentModel()
        new_model.set_from_revision(attribute_dict)
        self.update_from_model(new_model)

    def analyze(self):
        pass  # ta.analyze(self.model.content.value)

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

    def delete(self):
        """
        Delete model in store, as old versions models.
        :return:
        """
        index_storer.delete(self.model, self.old_versions)
        logger.log('WARN_DOC_DELETED', self.model.id.value, self.url)

    def _is_uptodate(self, update_time: float):
        date = self.model.doc_update_time.value if self.model.doc_update_time.initialized else self.model.doc_publication_time.value
        return date >= update_time

    @staticmethod
    def _check_and_truncate_url(url) -> str:
        """
        Check URL syntax.
        :return: Result of the check.
        """
        if not validators.url(url):
            logger.log('WARN_DOMAIN_MALFORMED', url)
            raise ValueError
        domain = get_domain(url)
        # Validate domain is supported
        known_media.get_media_by_domain(domain)
        url_regex = re.compile(r'^(.*?)(?:\?|$)')
        match = url_regex.match(url)
        return match.group(1)
