#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from src.media.known_media import KnownMedia
from src.store.document_storer import DocumentStorer
from src.gathering.html_document_gatherer import HTMLDocumentGatherer
from src.models.document_model import DocumentModel


class Document(object):
    DEFAULT_ES_HOSTS = '127.0.0.1:1080'

    def __init__(self, store_hosts=None, **kwargs):
        self.model = DocumentModel()

        self.extractor = None

        self.storer = None
        self.store_hosts = store_hosts if store_hosts else self.DEFAULT_ES_HOSTS
        self.store_kwargs = kwargs

        self.gatherer = None
        self.renderer = None

    def gather(self, url):
        if not self.gatherer:
            self.gatherer = HTMLDocumentGatherer(self.model, url)
        self.gatherer.gather()

    def extract_fields(self):
        if not self.extractor:
            extractor = KnownMedia()[self.model.domain]
            self.extractor = extractor(self.model)
        self.extractor.extract_fields()

    def store(self, doc_id: str=None):
        if not self.storer:
            self.storer = DocumentStorer(self.store_hosts, **self.store_kwargs)
        return self.storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str):
        if not self.storer:
            self.storer = DocumentStorer(self.store_hosts, **self.store_kwargs)
        self.model = self.storer.retrieve(doc_id)

    def update(self):
        if not self.storer:
            self.storer = DocumentStorer(self.store_hosts, **self.store_kwargs)
        self.storer.update(self.model)
