#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from src.media.known_media import KnownMedia
from src.store.document_storer import DocumentStorer
from src.rendering.document_renderer import DocumentRenderer
from src.gathering.html_document_gatherer import HTMLDocumentGatherer
from src.models.document_model import DocumentModel


class Document(object):
    def __init__(self):
        self.model = DocumentModel()

        self.extractor = None
        self.storer = None
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

    def store(self, doc_id: str=None, hosts=None, **kwargs):
        if not self.storer:
            self.storer = DocumentStorer(hosts, **kwargs)
        return self.storer.store(self.model, doc_id)

    def retrieve(self, doc_id: str, hosts=None, **kwargs):
        if not self.storer:
            storer = DocumentStorer(hosts, **kwargs)
        self.model = self.storer.retrieve(doc_id)

    def render_attribute(self, attribute: str) -> str:
        if not self.renderer:
            self.renderer = DocumentRenderer(self.model)
        return self.renderer.render_attribute(attribute)

    def update_attrbute(self, attribute: str, value: str):
        if not self.renderer:
            self.renderer = DocumentRenderer(self.model)
        self.renderer.update_attribute(attribute, value)
