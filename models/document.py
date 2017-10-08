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
    def __init__(self):
        self.model = DocumentModel()

        self.extractor = None
        self.storer = None
        self.gatherer = None

    def gather(self, url):
        self.gatherer = HTMLDocumentGatherer(self.model, url)
        self.gatherer.gather()

    def extract_fields(self):
        extractor = KnownMedia()[self.model.domain]
        self.extractor = extractor(self.model)

    def store(self, doc_id: str=None, hosts=None, **kwargs):
        storer = DocumentStorer(hosts, **kwargs)
        return storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str, hosts=None, **kwargs):
        storer = DocumentStorer(hosts, **kwargs)
        self.model = storer.retrieve(doc_id)

    def update(self, model: DocumentModel):
        self.model.update(model)
