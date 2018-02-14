#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime
from src.models.document_model import DocumentModel


class HTMLDocumentGatherer(object):
    """
    Class is used to gather an HTML document from an URL.
    """

    def __init__(self, dm: DocumentModel, url: str):
        """
        Class initializer
        :param dm: Document in which we will write gathering results.
        :param url: base URL for document gathering.
        """
        self.dm = dm
        self.url = url

    def gather(self):
        """
        Gather document from an URL.
        :return: HTML content located at URL
        """
        try:
            self._check_url()
            r = requests.get(self.url)
            self.dm.url = r.url
            self.dm.content = r.text
        except (ValueError, ConnectionError):
            raise

    def _check_url(self) -> bool:
        """
        Check URL syntax.
        :return: Result of the check.
        """
        # TODO
        if not self.url:
            raise ValueError
        return True

