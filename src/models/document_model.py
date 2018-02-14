#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements DocumentModel class.
"""

import re
from src.models.attribute import Attribute, StringListAttribute, StringAttribute,\
    DateAttribute, BooleanAttribute, IntegerAttribute
from collections import OrderedDict
from datetime import datetime
from copy import copy


class DocumentModel(object):
    """
    This class is a model which contains all possible attributes of a document.
    """
    def __init__(self) -> None:
        """ Ordered dict containing attributes """
        self.attributes = OrderedDict({
            'id': StringAttribute(desc="Identifiant", revisable=False, extractible=False, storable=False),
            'media': StringAttribute(desc="Média", revisable=False, storable='keyword'),
            'gather_time': DateAttribute(desc="Date de collecte de l'article", revisable=False, extractible=False,
                                         value=datetime.now()),
            'update_time': DateAttribute(desc="Date de révision", revisable=False, extractible=False,
                                         value=datetime.now()),
            'version_no': IntegerAttribute(desc="Numéro de version", revisable=False, extractible=False, value=1),
            'url': StringAttribute(desc="URL de l'article", extractible=False, storable='keyword'),

            # Buffer data
            'content': StringAttribute(desc="Contenu", displayable=False, revisable=False, extractible=False,
                                       storable=False),
            'body': StringAttribute(desc="Body", displayable=False, revisable=False, storable=False),

            # Extracted data
            'category': StringAttribute(desc="Catégorie", storable='keyword'),
            'title': StringAttribute(desc="Titre"),
            'description': StringAttribute(desc="Description"),
            'doc_publication_time': DateAttribute(desc="Date de publication de l'artice"),
            'doc_update_time': DateAttribute(desc="Date de mise à jour de l'article"),

            'href_sources': StringListAttribute(desc="Sources en lien hypertexte"),
            'explicit_sources': StringListAttribute(desc="Sources explicites"),
            'quoted_entities': StringListAttribute(desc="Entités citées"),
            'contains_private_sources': BooleanAttribute(desc="Sources privées"),
        })

    def __getattr__(self, item: str) -> Attribute:
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
    def domain(self) -> str:
        """
        Domain property extracts domain from url.
        :return: Web domain from which document was gathered.
        """
        domain_regex = re.compile(r'https?://(.*?)/')
        try:
            match = domain_regex.match(str(self.url))
            return match.group(1)
        except AttributeError:
            raise ValueError

    def update(self, model: 'DocumentModel') -> 'OldDocumentModel':
        """
        Updates model with another model : new values are set in current model, then old ones are returned
        in another model.
        :param model: model with newer values
        :return: old model only containing old values
        """
        old_model = OldDocumentModel(self.id.value)

        for k, v in model.attributes.items():
            if v.revisable and v.initialized and v.value != self.attributes[k].value:
                old_model.attributes[k] = copy(self.attributes[k])
                self.attributes[k].value = v.value

        # Updating update_time
        old_model.update_time.update(self.update_time.value)
        self.update_time.update(model.update_time.value)

        # Updating version_no
        old_model.version_no.update(self.version_no.value)
        self.version_no.value += 1

        return old_model

    def render_for_store(self) -> dict:
        """
        Render model as a body for storing its content.
        :return: storable body filled with attributes data
        """
        body = {}
        for k, v in self.attributes.items():
            if v.storable:
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

    def set_from_display(self, attribute_dict: dict):
        """
        Fill revisable attribute values from a display (web form).
        :param attribute_dict: dict with values originating from display
        :return:-
        """
        for k, v in self.attributes.items():
            if v.revisable and k in attribute_dict:
                v.set_from_display(attribute_dict[k])


class OldDocumentModel(DocumentModel):
    """
    Model version containing old versions of attributes.
    """
    def __init__(self, doc_id) -> None:
        super(OldDocumentModel, self).__init__()

        self.attributes['doc_id'] = StringAttribute(desc="Identifiant du document", displayable=False,
                                                    revisable=False, extractible=False, storable='keyword',
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
