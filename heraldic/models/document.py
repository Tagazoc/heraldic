#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Document class.
"""

from heraldic.media.known_media import known_media
from heraldic.store import index_storer, index_searcher
from heraldic.models.document_model import DocumentModel
from typing import List
import heraldic.misc.exceptions as ex
from heraldic.misc.logging import logger
from heraldic.misc.functions import get_domain, get_truncated_url
from heraldic.analysis.text_analyzer import ta
from heraldic.misc.config import config
import itertools


class Document(object):
    """
    Class representing a Document through its way through Heraldic.
    """
    def __init__(self, url: str='', doc_id: str=None, debug=False):
        self.model: DocumentModel = DocumentModel()
        self.old_versions: List[DocumentModel] = []
        self.url = self._check_and_truncate_url(url) if url else ''
        self.doc_id = doc_id
        # TODO sortir l'id du model ?
        if doc_id:
            try:
                self._retrieve()
            except ex.DocumentNotFoundException:
                self.retrieve_url_from_parse_error()
        elif url:
            try:
                self.retrieve_from_url()
            except ex.DocumentNotFoundException:
                self.retrieve_id_from_parse_error()
        self.debug = debug
        self.extractor = None

    @classmethod
    def from_model(cls, model):
        doc = cls()
        doc.model = model
        doc.url = model.urls.value[0]
        return doc

    def gather(self, update_time=None, update: bool=False, filepath: str= ''):
        """
        Gather a document contents from an url, parse it and store or update it.
        :param update_time: Update time (in rss feed) to avoid gathering if up-to-date
        :param update: disable existence check, in order to override document
        :param filepath: If document is gathered from a file, file path.
        """
        if self.model.initialized:
            # It is an update, is it already up-to-date ? Unless override flag
            if not update and (not update_time or self._is_uptodate(update_time)):
                raise ex.DocumentExistsException(self.url)
            updated_model = DocumentModel()
            if filepath:
                updated_model.gather_from_file(self.url, filepath)
            else:
                final_url = updated_model.gather_from_url(self.url)
                self.model.urls.append(self._check_and_truncate_url(final_url))
            self._extract_fields(updated_model)
            if config['DEFAULT'].getboolean('extract_words'):
                updated_model.words.update(ta.extract_words(updated_model.body.value))
            self.update_from_model(updated_model)
            logger.log('INFO_DOC_UPDATE_SUCCESS', self.url)
        else:
            if filepath:
                self.model.gather_from_file(self.url, filepath)
            else:
                final_url = self.model.gather_from_url(self.url)
                self.model.urls.append(self._check_and_truncate_url(final_url))

            try:
                self._extract_fields()
            except ex.MandatoryParsingException:
                self._store_failed_parsing_error()
                raise
            if config['DEFAULT'].getboolean('extract_words'):
                self.model.words.update(ta.extract_words(self.model.body.value))
            self._store()
            logger.log('INFO_DOC_STORE_SUCCESS', self.url)

    def _extract_fields(self, model=None):
        """
        Find document media and extract document fields according to it.
        :return:
        """
        model = model if model is not None else self.model
        if not self.extractor:
            extractor = known_media.get_media_by_domain(get_domain(self.url))
            self.extractor = extractor(model)
        self.extractor.extract_fields(debug=self.debug)

    def _store(self):
        """
        Store document contents.
        :return:
        """
        self.model.id = index_storer.store(self.model, self.doc_id)

    def _retrieve(self):
        """
        Retrieve document contents from a store.
        """
        self.model = index_searcher.retrieve_model(self.doc_id)
        self.url = self.model.urls.value[0]

    def retrieve_from_url(self):
        """
        Retrieve a document from its URL.
        """
        self.model = index_searcher.retrieve_model_from_url(self.url)

    def retrieve_old_versions(self):
        """
        Retrieve old versions of a document from its ID.
        """
        self.old_versions = list(index_searcher.retrieve_old_version_models(self.model.id.value))
        self._set_attributes_versions()

    def retrieve_id_from_parse_error(self):
        """
        Retrieve the ID of a parse error from the document's URL.
        :return:
        """
        self.doc_id = index_searcher.search_error_id_by_url(self.url)

    def retrieve_url_from_parse_error(self):
        """
        Retrieve the ID of a parse error from the document's URL.
        :return:
        """
        self.url = index_searcher.retrieve_error_url(self.doc_id)

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

    def _set_attributes_versions(self):
        """
        Set version for each attribute : it is not trivial as only old values are stored in old versions models,
        so the attribute's version does not equal the model's version.
        :return:
        """
        counter_dict = {}
        for model in itertools.chain(self.old_versions, [self.model]):
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

    def _store_failed_parsing_error(self):
        index_storer.store_failed_parsing_error(self.model, self.doc_id)

    def delete(self):
        """
        Delete model in store, as old versions models.
        :return:
        """
        index_storer.delete(self.model, self.old_versions)
        logger.log('WARN_DOC_DELETED', self.model.id.value, self.url)

    def _is_uptodate(self, update_time: float):
        date = self.model.doc_update_time.value if self.model.doc_update_time.initialized \
            else self.model.doc_publication_time.value
        return date >= update_time

    @staticmethod
    def _check_and_truncate_url(url) -> str:
        """
        Check URL syntax.
        :return: Result of the check.
        """
        domain = get_domain(url)

        # Validate domain is supported
        known_media.get_media_by_domain(domain)

        return get_truncated_url(url)
