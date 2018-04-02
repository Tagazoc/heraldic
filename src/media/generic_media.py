#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing generic DocumentExtractor class.
"""

from typing import List
import html
from src.models.document_model import DocumentModel
from bs4 import BeautifulSoup
from src.store import index_searcher
from datetime import datetime
from src.heraldic_exceptions import ParsingFailureException, HTMLParsingFailureException, DateFormatFailureException
from src.misc.logging import logger
import re


def handle_parsing_errors(decorated):
    def wrapper(self):
        try:
            result = decorated(self)
        except AttributeError:
            raise HTMLParsingFailureException
        except TypeError:
            raise HTMLParsingFailureException
        return result

    return wrapper


class GenericMedia(object):
    """
        Generic class for attribute extraction from a document, should not be directly instanciated.
    """
    domains = ['www.heraldic-project.org', 'hrldc.org']
    """The domains used in URLs of the selected media"""
    id = 'generic'
    display_name = 'Generic'

    def __init__(self, dm: DocumentModel) -> None:
        """
        Initialize extractor by parsing HTML contained in document model.

        :param dm: Document model which will contain all extracted items.
        """
        self.html_soup = BeautifulSoup(dm.content.render_for_display(), "html.parser")
        self.dm = dm

    @classmethod
    def get_document_count(cls) -> int:
        return index_searcher.count(q='media:' + cls.id)

    def extract_fields(self):
        """
        This function calls every extraction function supported by the media.
        """
        for k, v in self.dm.attributes.items():
            if v.extractible:
                try:
                    func = getattr(self, "_extract_" + k)
                    v.set_from_extraction(func())
                except ParsingFailureException as err:
                    logger.log('WARN_ATTRIBUTE_PARSING_ERROR', k, self.dm.urls.value[0], err.message)
                    v.parsing_error = err.message

    def _extract_media(self) -> str:
        """
        Function which returns media name attribute, in order to work with extract_fields function.
        :return: Media name
        """
        return self.id

    @handle_parsing_errors
    def _extract_title(self) -> str:
        """
        Extract HTML title (in <head> block) from HTML content.
        :return: HTML title
        """
        return html.unescape(self.html_soup.head.title.text)

    @handle_parsing_errors
    def _extract_description(self) -> str:
        """
        Extract description (in meta tag, in <head> block) from HTML content.
        :return: HTML description
        """
        return html.unescape(self.html_soup.head.find('meta', attrs={"name": "description"})['content'])

    @handle_parsing_errors
    def _extract_body(self) -> str:
        """
        Extract document body (not HTML body of course, if it is an article this will return
        only article body.
        :return: Document body
        """
        return ''

    @handle_parsing_errors
    def _extract_doc_publication_time(self) -> datetime:
        """
        Extract document date and time (if present) of publication.
        :return: Document publication date and time as timestamp
        """
        time_text = self.html_soup.find('meta', attrs={'property': "article:published_time"}).get('content')
        try:
            time_text = re.sub(r'\+\d{2}:\d{2}', '', time_text)
            pub_time = datetime.strptime(time_text, '%Y-%m-%dT%H:%M:%S')
        except ValueError as err:
            raise DateFormatFailureException(err.args[0])
        return pub_time

    @handle_parsing_errors
    def _extract_doc_update_time(self) -> datetime:
        """
        Extract document date and time (if present) about when it was updated.
        :return: Document update date and time as timestamp
        """
        time_text = self.html_soup.find('meta', attrs={'property': "article:modified_time"}).get('content')
        try:
            time_text = re.sub(r'\+\d{2}:\d{2}', '', time_text)
            pub_time = datetime.strptime(time_text, '%Y-%m-%dT%H:%M:%S')
        except ValueError as err:
            raise DateFormatFailureException(err.args[0])
        return pub_time

    @handle_parsing_errors
    def _extract_href_sources(self) -> List[str]:
        """
        Extract sources displayed as links from the document.
        :return: list of sources contained in the document
        """
        return []

    @handle_parsing_errors
    def _extract_category(self) -> str:
        """
        Extract category as given by the media (specialized media may have only one category).
        :return: the category of the document
        """
        return ''

    @handle_parsing_errors
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

    @staticmethod
    def _format_datetime(string: str, format_string: str) -> datetime:
        try:
            date = datetime.strptime(string, format_string)
        except ValueError as err:
            raise DateFormatFailureException from err
        return date
