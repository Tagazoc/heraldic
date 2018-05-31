#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements DocumentModel class.
"""

from src.models.attribute import Attribute, StringListAttribute, StringAttribute,\
    DateAttribute, BooleanAttribute, IntegerAttribute, WordListAttribute
from collections import OrderedDict
from copy import copy
from typing import Dict, Optional
import requests
from datetime import datetime


class DocumentModel(object):
    """
    This class is a model which contains all possible attributes of a document.
    """
    def __init__(self) -> None:
        """ Ordered dict containing attributes """
        self.attributes: Dict[str, Attribute] = OrderedDict([
            ('id', StringAttribute(desc="Identifiant", revisable=False, extractible=False, storable=False)),
            ('media', StringAttribute(desc="Média", revisable=False, storable={'type': 'keyword'})),
            ('gather_time', DateAttribute(desc="Date de collecte de l'article", revisable=False, extractible=False)),
            ('update_time', DateAttribute(desc="Date de révision", revisable=False, extractible=False)),
            ('version_no', IntegerAttribute(desc="Numéro de version", revisable=False, extractible=False)),
            ('urls', StringListAttribute(desc="URLs de l'article", extractible=False, revisable=False,
                                         storable='keyword')),

            # Buffer data
            ('content', StringAttribute(desc="Contenu", displayable=False, revisable=False, extractible=False,
                                        storable=False)),
            ('body', StringAttribute(desc="Body", displayable=False, revisable=False, storable=False, mandatory=True)),

            # Words !
            ('words', WordListAttribute(desc="Words", displayable=True, revisable=True, extractible=False)),

            # Extracted data
            ('category', StringAttribute(desc="Catégorie", revisable=False, storable={'type': 'keyword'})),
            ('title', StringAttribute(desc="Titre", revisable=False)),
            ('description', StringAttribute(desc="Description", revisable=False)),
            ('doc_publication_time', DateAttribute(desc="Date de publication de l'article", revisable=False)),
            ('doc_update_time', DateAttribute(desc="Date de mise à jour de l'article", revisable=False)),

            ('keywords', StringListAttribute(desc="Mots-clés de l'article", revisable=False)),
            ('href_sources', StringListAttribute(desc="Sources en lien hypertexte", revisable=False)),
            ('explicit_sources', StringListAttribute(desc="Sources explicites")),
            ('quoted_entities', StringListAttribute(desc="Entités citées", extractible=False)),
            ('contains_private_sources', BooleanAttribute(desc="Sources privées", extractible=False)),
            ('subscribers_only', BooleanAttribute(desc="Réservé aux abonnés", revisable=False))
        ])

        self.from_gathering = False
        """ Whether this model comes from document gathering (or revision). """

        self.storable_values_updated = False
        """ Whether some values did change during model update. """

    def __getattr__(self, item: str) -> Optional[Attribute]:
        """
        Shortcut for accessing attributes, for example : dm.media
        :param item: attribute name
        :return: attribute
        """
        try:
            attributes = self.__getattribute__('attributes')
            return attributes[item]
        except AttributeError:
            return None

    def __setattr__(self, key: str, value: str):
        """
        Shortcut for setting attribute value
        :param key: attribute name
        :param value: future attribute value
        :return:
        """
        if self.attributes and key in self.attributes.keys():
            self.attributes[key].value = value
        else:
            super(DocumentModel, self).__setattr__(key, value)

    @property
    def initialized(self):
        return self.urls.value != []

    def update(self, model: 'DocumentModel') -> 'OldDocumentModel':
        """
        Updates model with another model : new values are set in current model, then old ones are returned
        in another model.
        :param model: model with newer values
        :return: old model only containing old values
        """
        old_model = OldDocumentModel(self.id.value)
        storable_values_updated = False

        filter_attr = 'extractible' if model.from_gathering else 'revisable'

        for k, v in model.attributes.items():
            if v.__getattribute__(filter_attr):
                if v.initialized and v.value != self.attributes[k].value:
                    if v.storable:
                        storable_values_updated = True
                    old_model.attributes[k].update(self.attributes[k].value)
                    self.attributes[k] = copy(v)

                elif v.parsing_error is not None or v.suggestions != self.attributes[k].suggestions:
                    # Updating attribute even if value did not change
                    self.attributes[k] = copy(v)

        # Did some values really change ?
        self.storable_values_updated = storable_values_updated

        # Updating update_time
        old_model.attributes['update_time'] = copy(self.update_time)
        self.attributes['update_time'].value = datetime.now()

        # Updating version_no
        old_model.version_no = copy(self.version_no.value)
        self.version_no.value += 1

        # Updating from_gathering attribute
        self.from_gathering = model.from_gathering

        return old_model

    def render_for_store(self) -> dict:
        """
        Render model as a body for storing its content.
        :return: storable body filled with attributes data
        """
        body = {}
        for k, v in self.attributes.items():
            if v.storable and v.initialized:
                body[k] = v.render_for_store()
        return body

    def set_from_store(self, attribute_dict: dict):
        """
        Fill storable attribute values from a store.
        :param attribute_dict: Dict retrieved from a store
        :return:
        """
        for k, v in self.attributes.items():
            if v.storable and k in attribute_dict:
                v.set_from_store(attribute_dict[k])

    def set_from_revision(self, attribute_dict: dict):
        """
        Fill revisable attribute values from a display (web form).
        :param attribute_dict: dict with values originating from display
        :return:-
        """
        for k, v in self.attributes.items():
            if v.revisable and k in attribute_dict:
                v.set_from_display(attribute_dict[k])

    @property
    def errors(self):
        error_dict = {}
        for k, v in self.attributes.items():
            if v.parsing_error is not None:
                error_dict[k] = v.parsing_error
        return error_dict

    @property
    def suggestions(self):
        suggestions_dict = {}
        for k, v in self.attributes.items():
            if v.suggestions:
                suggestions_dict[k] = v.suggestions
        return suggestions_dict

    @property
    def has_suggestions(self):
        return not self.suggestions == {}

    @property
    def has_errors(self):
        return not self.errors == {}

    def render_errors_for_store(self):
        return self.errors

    def render_suggestions_for_store(self):
        return self.suggestions

    def set_errors_from_store(self, error_dict: dict):
        for k, v in self.attributes.items():
            if k in error_dict.keys():
                v.parsing_error = error_dict[k]

    def set_suggestions_from_store(self, suggestions_dict: dict):
        for k, v in self.attributes.items():
            if k in suggestions_dict.keys():
                v.suggestions = suggestions_dict[k]

    def gather_from_url(self, url: str) -> str:
        """
        Gather document from an URL.
        :return: Final URL of the document.
        """
        try:
            r = requests.get(url)
        except (ValueError, ConnectionError):
            raise
        # Setting final URL (in case of redirection)
        urls: StringListAttribute = self.attributes['urls']
        urls.append(url)
        r.encoding = 'utf-8'
        self.attributes['content'].value = r.text

        self._set_gather_attributes()
        return r.url

    def gather_from_file(self, url: str, filepath: str):
        urls: StringListAttribute = self.attributes['urls']
        urls.append(url)

        with open(filepath, 'r') as f:
            self.attributes['content'].value = f.read()
        self._set_gather_attributes()

    def _set_gather_attributes(self):

        # Setting gather time in model
        self.attributes['gather_time'].value = datetime.now()

        # Unless we use the model to update another document, its version is 1.
        self.attributes['version_no'].value = 1

        # Specify model comes from gathering.
        self.from_gathering = True


class OldDocumentModel(DocumentModel):
    """
    Model version containing old versions of attributes.
    """
    def __init__(self, doc_id) -> None:
        super(OldDocumentModel, self).__init__()

        self.attributes['doc_id'] = StringAttribute(desc="Identifiant du document", displayable=False,
                                                    revisable=False, extractible=False, storable={'type': 'keyword'},
                                                    initialized=True, value=doc_id)
        """ Associated up-to-date document identifier. """

    def render_for_store(self) -> dict:
        """
        Render model as a body for storing its content ; uninitialized values are not stored for old versions.
        :return: storable body filled with attributes data
        """
        body = {}
        for k, v in self.attributes.items():
            if v.storable and v.initialized:
                body[k] = v.render_for_store()
        return body
