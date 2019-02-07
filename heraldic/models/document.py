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
from heraldic.misc.functions import get_domain
from heraldic.analysis.text_analyzer import ta
from heraldic.misc.config import config
import itertools


class Document(object):
    """
    Class representing a Document through its way through Heraldic.
    """
    def __init__(self, url: str='', doc_id: str=None, filepath: str=''):
        self.model: DocumentModel = DocumentModel()
        self.old_versions: List[DocumentModel] = []
        self.url = ''
        if url:
            self._check_domain_support(url)
            self.url = url
        self.doc_id = doc_id
        self.filepath = filepath

        if doc_id:
            try:
                self._retrieve()
            except ex.DocumentNotFoundException:
                self.retrieve_url_from_parse_error()
                self.model = DocumentModel()
        elif url:
            try:
                self.retrieve_from_url()
            except ex.DocumentNotFoundException:
                self.retrieve_id_from_parse_error()
                self.model = DocumentModel()

    @classmethod
    def from_model(cls, model):
        doc = cls()
        doc.model = model
        doc.url = model.urls.value[0]
        return doc

    def gather(self, update_time=None, update: bool=False, raise_on_optional=False):
        """
        Gather a document contents from an url, parse it and store or update it.
        :param update_time: Update time (in rss feed) to avoid gathering if up-to-date
        :param update: disable existence check, in order to override document
        :param raise_on_optional: Raise exception on optional parsing if encountered
        """
        if self.model.initialized:
            # It is an update, is it already up-to-date ? Unless override flag
            if not update and (not update_time or self._is_uptodate(update_time)):
                raise ex.DocumentExistsException(self.url)

            updated_model = self._fetch_and_extract(raise_on_optional=raise_on_optional)
            self.update_from_model(updated_model)
            logger.log('INFO_DOC_UPDATE_SUCCESS', self.url)
        else:
            # If URL was a redirection, try to retrieve it aswell
            model = self._fetch_and_extract(raise_on_optional=raise_on_optional)
            if len(model.urls.value) > 1:
                # If it already exists, update it
                try:
                    self.retrieve_from_url()
                    self.update_from_model(model)
                    logger.log('INFO_DOC_UPDATE_SUCCESS', self.url)
                    return
                except ex.DocumentNotFoundException:
                    self.retrieve_id_from_parse_error()
            self.model = model
            self._store()
            logger.log('INFO_DOC_STORE_SUCCESS', self.url)

    def _fetch_and_extract(self, raise_on_optional=False) -> DocumentModel:
        model = DocumentModel()
        if self.filepath:
            model.gather_from_file(self.url, self.filepath)
        else:
            model.gather_from_url(self.url)
            self._check_domain_support(model.final_url)
        try:
            self._extract_fields(model=model, raise_on_optional=raise_on_optional)
        except ex.MandatoryParsingException:
            self._store_failed_parsing_error(model)
            raise
        if config['DEFAULT'].getboolean('extract_words'):
            model.words.update(ta.extract_words(model.body.value))
        return model

    def _extract_fields(self, model=None, raise_on_optional=False):
        """
        Find document media and extract document fields according to it.
        :return:
        """
        model = model if model is not None else self.model

        media_class = known_media.get_media_class_by_domain(get_domain(model.final_url))
        if not media_class.is_url_article(model.final_url):
            if self.doc_id:
                self._delete_error()
            raise ex.UrlNotSupportedException(self.url, model.final_url)
        # Process each extractor, finishing with those set as "default"
        for extractor_class in sorted(media_class.get_extractors(), key=lambda t: 1 if t.default_extractor else 0):
            extractor = extractor_class(model)
            if extractor.check_extraction():
                extractor.extract_fields(raise_on_optional=raise_on_optional)
                return
        # URL is not supported, so delete the error if any
        if self.doc_id:
            self._delete_error()
        raise ex.UrlNotSupportedException(self.url, model.final_url)

    def _store(self):
        """
        Store document contents.
        :return:
        """
        self.model.id.value = index_storer.store(self.model, self.doc_id)

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
        self.doc_id = self.model.id.value

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

    def _store_failed_parsing_error(self, model: DocumentModel):
        index_storer.store_failed_parsing_error(model, self.doc_id)

    def delete(self):
        """
        Delete model in store, as old versions models.
        :return:
        """
        index_storer.delete(self.model, self.old_versions)
        logger.log('WARN_DOC_DELETED', self.model.id.value, self.url)

    def _delete_error(self):
        index_storer.delete_error(self.doc_id)

    def _is_uptodate(self, update_time: float):
        date = self.model.doc_update_time.value if self.model.doc_update_time.initialized \
            else self.model.doc_publication_time.value
        return date >= update_time

    def __str__(self):
        display_str = ''
        for k, v in self.model.attributes.items():
            if v.extractible:
                if v.parsing_error:
                    display_str += k + ' - ' + v.parsing_error + "\n"
                else:
                    display_str += k + ' : ' + v.render_for_display() + "\n"
                if v.suggestions:
                    display_str += k + ' : suggestions : ' + ",".join(v.render_suggestions_for_display()) + "\n"
        return display_str

    @staticmethod
    def _check_domain_support(url) -> str:
        """
        Check URL syntax, then remove protocol scheme, port and URL resource.
        :return: Result of the check.
        """
        domain = get_domain(url)

        # Validate domain is supported
        known_media.get_media_class_by_domain(domain)
