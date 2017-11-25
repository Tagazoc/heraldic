#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

import re
from src.models.attribute import IntegerAttribute, StringListAttribute, StringAttribute,\
    DateAttribute, BooleanAttribute
from collections import OrderedDict


class DocumentModel(object):
    """
    This class is a model which contains all possible attributes of a document.
    """
    def __init__(self):
        # Structural data
        self.attributes = OrderedDict({
            'id': IntegerAttribute(desc="Identifiant", displayable=False, revisable=False, extractible=False),
            'media': StringAttribute(desc="Média", revisable=False),
            'gather_time': DateAttribute(desc="Date de collecte du document", revisable=False, extractible=False),
            'update_time': DateAttribute(desc="Date de révision", revisable=False, extractible=False),
            'url': StringAttribute(desc="URL de l'article", extractible=False),

            # Buffer data
            'content': StringAttribute(desc="Contenu", displayable=False, revisable=False, extractible=False),
            'body': StringAttribute(desc="Body", displayable=False, revisable=False),

            # Extracted data
            'category': StringAttribute(desc="Catégorie"),
            'title': StringAttribute(desc="Titre"),
            'description': StringAttribute(desc="Description"),
            'doc_publication_time': DateAttribute(desc="Date de publication de l'artice"),
            'doc_update_time': DateAttribute(desc="Date de mise à jour de l'article"),

            'href_sources': StringListAttribute(desc="Sources en lien hypertexte"),
            'explicit_sources': StringListAttribute(desc="Sources explicites"),
            'quoted_entities': StringListAttribute(desc="Entités citées"),
            'contains_private_sources': BooleanAttribute(desc="Sources privées"),
        })

    def __getattr__(self, item):
        try:
            attributes = self.__getattribute__('attributes')
            return attributes[item]
        except AttributeError:
            return None

    def __setattr__(self, key, value):
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
