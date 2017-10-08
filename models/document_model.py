#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from datetime import datetime
import re


class DocumentModel(object):
    """
    This class is a model which contains all possible attributes of a document.
    """
    def __init__(self):
        # Structural data
        self.id = None
        self.media = ''
        self.gather_time = datetime.now()
        self.update_time = datetime.now()
        self.url = ''

        # Buffer data
        self.content = ''
        self.body = ''

        # Extracted data
        self.category = ''
        self.title = ''
        self.description = ''
        self.quotes = []
        self.href_sources = []
        self.doc_publication_time = datetime.now()
        self.doc_update_time = datetime.now()
        self.explicit_sources = []

    @property
    def domain(self) -> str:
        """
        Domain property extracts domain from url.
        :return: Web domain from which document was gathered.
        """
        domain_regex = re.compile(r'https?://(.*?)/')
        try:
            match = domain_regex.match(self.url)
            return match.group(1)
        except AttributeError:
            raise ValueError

    def update(self, model: 'DocumentModel'):
        """
        Update model with another. Some attributes will not be updated : id, gather_date.
        :param model: Update source model
        """
        self.title = model.title
        self.description = model.description
        self.url = model.url
        self.media = model.media
        self.content = model.content
        self.category = model.category
        self.body = model.body
        self.quotes = model.quotes
        self.href_sources = model.href_sources
        self.doc_publication_time = model.doc_publication_time
        self.doc_update_time = model.doc_update_time
        self.explicit_sources = model.explicit_sources
