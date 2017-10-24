#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generic document for media extractor implementation.
"""

from typing import List
import html
from src.models.document_model import DocumentModel
import re
from bs4 import BeautifulSoup
from datetime import datetime


class GenericMediaExtractor(object):
    """
        Generic class for item extraction from a document, should not be directly instanciated.
    """
    domains = ['www.heraldic-project.org', 'hrldc.org']
    """The domains used in URLs of the selected media"""
    media_name = 'generic'

    def __init__(self, dm: DocumentModel) -> None:
        """
        Class initializer.

        :param dm: Document model which will contain all extracted items.
        """
        self.html_soup = BeautifulSoup(dm.content, "html.parser")
        self.dm = dm

        self._extract_fields()

    def _extract_fields(self):
        """
        This function calls every extraction supported by the media.
        """
        self.dm.media = self.media_name
        self.dm.title = self._extract_html_title()
        self.dm.description = self._extract_html_description()
        self.dm.body = self._extract_document_body()
        self.dm.href_sources = self._extract_href_sources()
        self.dm.explicit_sources = self._extract_explicit_sources()
        self.dm.category = self._extract_category()
        self.dm.doc_publication_time = self._extract_publication_timestamp()
        self.dm.doc_update_time = self._extract_update_timestamp()

    def _extract_html_title(self) -> str:
        """
        Extract HTML title (in <head> block) from HTML content.
        :return: HTML title
        """
        return html.unescape(self.html_soup.head.title.text)

    def _extract_html_description(self) -> str:
        """
        Extract description (in meta tag, in <head> block) from HTML content.
        :return: HTML description
        """
        return html.unescape(self.html_soup.head.find('meta', attrs={"name": "description"})['content'])

    def _extract_document_body(self) -> str:
        """
        Extract document body (not HTML body of course, if it is an article this will return
        only article body.
        :return: Document body
        """
        return ''

    def _extract_publication_timestamp(self) -> datetime:
        """
        Extract document date and time (if present) of publication.
        :return: Document publication date and time as timestamp
        """
        return datetime.now()

    def _extract_update_timestamp(self) -> datetime:
        """
        Extract document date and time (if present) about when it was updated.
        :return: Document update date and time as timestamp
        """
        return datetime.now()

    def _extract_href_sources(self) -> List[str]:
        """
        Extract sources displayed as links from the document.
        :return: list of sources contained in the document
        """
        return []

    def _extract_category(self) -> str:
        """
        Extract category as given by the media (specialized media may have only one category).
        :return: the category of the document
        """
        return ''

    def _extract_explicit_sources(self) -> List[str]:
        """
        Extract sources explicitly given in the document
        :return: list of the explicit sources
        """
        return []

    @staticmethod
    def _exclude_hrefs(html_as: List, attribute: str, value: str, parent=False):
        """
        # Exclude links with specific attribute, as they are additional links
        :param html_as:
        :param attribute:
        :param value:
        :param parent:
        :return:
        """
        filtered_as = []
        for a in html_as:
            try:
                tag = a
                if parent:
                    tag = a.parent
                if value in tag[attribute]:
                    continue
            except KeyError:
                # No such attribute for <a> tag
                pass
            filtered_as.append(a)

        return filtered_as
