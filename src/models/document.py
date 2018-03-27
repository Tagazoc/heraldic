#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Document class.
"""

from src.media.known_media import known_media
from src.store import model_storer, model_searcher
from src.models.document_model import DocumentModel
from typing import List
from src.heraldic_exceptions import DocumentExistsException, DomainNotSupportedException
from src.misc.logging import logger
import validators
import re


class Document(object):
    """
    Class representing a Document during its way through Heraldic.
    """
    def __init__(self, url: str=''):
        self.model: DocumentModel = DocumentModel()
        self.old_versions: List[DocumentModel] = []
        self.url = ''
        if url:
            self.url = self._check_and_truncate_url(url)

        self.extractor = None

    def gather(self, update_time=None, override: bool=False, filepath: str=''):
        """
        Gather a document contents from an url, parse it and store or update it.
        :param update_time: Update time (in rss feed) to avoid gathering if up-to-date
        :param override: disable existence check, in order to override document
        :param filepath: Whether url is instead a file path.
        :return:
        """

        # TODO Après avoir tronqué les paramètres de l'URL originale du document (à mettre en attribut et à récupérer
        # dès la construction ?), on recherche cette URL dans l'index, puis on request,
        # durant lequel on ajoute l'URL originale
        # et l'URL finale aux URL du document (à passer en StringListAttribute) si absentes

        if self.model.url.value:
            # It is an update, is it already up-to-date ? Unless override flag
            if not override and update_time and self.model.doc_update_time.value\
                    and self.model.doc_update_time.value >= update_time:
                raise DocumentExistsException(self.url)
            up_d = Document()
            if filepath:
                up_d.model.gather_from_file(self.url, filepath)
            else:
                up_d.model.gather_from_url(self.url)
            up_d._extract_fields()
            self.update_from_model(up_d.model)
            logger.log('INFO_DOC_UPDATE_SUCCESS', self.url)
        else:
            if filepath:
                self.model.gather_from_file(self.url, filepath)
            else:
                self.model.gather_from_url(self.url)
            self._extract_fields()
            self.store()
            logger.log('INFO_DOC_STORE_SUCCESS', self.url)

    def _extract_fields(self):
        """
        Find document media and extract document fields according to it.
        :return:
        """
        if not self.extractor:
            extractor = known_media[self._get_domain(self.model.url.value)]
            self.extractor = extractor(self.model)
        self.extractor.extract_fields()

    def store(self, doc_id: str=None):
        """
        Store document contents.
        :param doc_id: ID of the document in the store
        :return:
        """
        self.model.id = model_storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str):
        """
        Retrieve document contents from a store.
        :param doc_id: ID of the document in the store
        """
        self.model = model_searcher.retrieve(doc_id)
        self.url = self.model.url.value

    def retrieve_from_url(self):
        """
        Retrieve a document from its URL.
        """
        self.model = model_searcher.retrieve_from_url(self.url)

    def retrieve_old_versions(self):
        """
        Retrieve old versions of a document from its ID.
        """
        self.old_versions = model_searcher.retrieve_old_versions(self.model.id.value)
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
        model_storer.delete(self.model, self.old_versions)
        logger.log('WARN_DOC_DELETED', self.model.id.value, self.model.url.value)

    @staticmethod
    def _get_domain(url):
        domain_regex = re.compile(r'https?://(.*?)/')
        try:
            match = domain_regex.match(url)
            return match.group(1)
        except AttributeError:
            raise ValueError

    @staticmethod
    def _check_and_truncate_url(url):
        """
        Check URL syntax.
        :return: Result of the check.
        """
        if not validators.url(url):
            logger.log('WARN_DOMAIN_MALFORMED', url)
            raise ValueError
        domain = Document._get_domain(url)
        if known_media[domain] is None:
            raise DomainNotSupportedException(domain)
        url_regex = re.compile(r'^(.*?)(?:\?|$)')
        match = url_regex.match(url)
        return match.group(1)
