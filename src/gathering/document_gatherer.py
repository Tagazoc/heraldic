#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from datetime import datetime
from src.models.document_model import DocumentModel
import validators


class DocumentGatherer(object):
    def __init__(self, dm):
        self.dm = dm

    def gather(self):
        pass


class HTTPDocumentGatherer(DocumentGatherer):
    """
    Class is used to gather an HTML document from an URL.
    """

    def __init__(self, dm: DocumentModel, url: str):
        """
        Class initializer
        :param dm: Document in which we will write gathering results.
        :param url: base URL for document gathering.
        """
        super(HTTPDocumentGatherer, self).__init__(dm)
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

            # Setting gather time in model
            self.dm.gather_time = datetime.now()

            # Unless we use the model to update another document, its version is 1.
            self.dm.version_no = 1

            # Specify model comes from gathering.
            self.dm.from_gathering = True
        except (ValueError, ConnectionError):
            raise

    def _check_url(self) -> bool:
        """
        Check URL syntax.
        :return: Result of the check.
        """
        return validators.url(self.url)


class FileDocumentGatherer(DocumentGatherer):
    def __init__(self, dm: DocumentModel, url: str, filepath: str):
        super(FileDocumentGatherer, self).__init__(dm)
        self.filepath = filepath
        self.url = url

    def gather(self):
        self.dm.url = self.url
        with open(self.filepath, 'r') as f:
            self.dm.content = f.read()
        # Setting gather time in model
        self.dm.gather_time = datetime.now()

        # Unless we use the model to update another document, its version is 1.
        self.dm.version_no = 1

        # Specify model comes from gathering.
        self.dm.from_gathering = True
