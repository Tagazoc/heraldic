#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing generic DocumentExtractor class.
"""

from typing import List, Optional
import html
from src.models.document_model import DocumentModel
from bs4 import BeautifulSoup
from src.store import index_searcher
from datetime import datetime
from src.misc.exceptions import OptionalParsingFailureException, HTMLOptionalParsingFailureException,\
    DateFormatOptionalFailureException, MandatoryParsingFailureException, InvalidUrlException
from src.misc.logging import logger
from src.misc.functions import get_truncated_url
import re


def optional_parsing_function(decorated):
    def wrapper(self, *args):
        try:
            result = decorated(self, *args)
        except Exception:
            raise HTMLOptionalParsingFailureException
        return result

    return wrapper


def mandatory_parsing_function(decorated):
    def wrapper(self, *args):
        try:
            result = decorated(self, *args)
        except Exception:
            raise MandatoryParsingFailureException
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

    def extract_fields(self, debug=False):
        """
        This function calls every extraction function supported by the media.
        """
        for k, v in self.dm.attributes.items():
            if v.extractible:
                try:
                    func = getattr(self, "_extract_" + k)
                    extracted_data = func()
                    try:
                        # Apply post-treatment if any
                        post_func = getattr(self, "_post_extract_" + k)
                        extracted_data = post_func(extracted_data)
                    except AttributeError:
                        pass
                    v.set_from_extraction(extracted_data)
                except OptionalParsingFailureException as err:
                    logger.log('WARN_ATTRIBUTE_PARSING_ERROR', k, self.dm.urls.value[0], err.message)
                    v.parsing_error = err.message
                    if debug:
                        raise
                except MandatoryParsingFailureException as err:
                    logger.log('WARN_MANDATORY_ATTRIBUTE_PARSING_ERROR', k, self.dm.urls.value[0], err.message)
                    raise

    def _extract_media(self) -> str:
        """
        Function which returns media name attribute, in order to work with extract_fields function.
        :return: Media name
        """
        return self.id

    @optional_parsing_function
    def _extract_title(self) -> str:
        """
        Extract HTML title (in <head> block) from HTML content.
        :return: HTML title
        """
        return html.unescape(self.html_soup.head.title.text)

    @optional_parsing_function
    def _extract_description(self) -> str:
        """
        Extract description (in meta tag, in <head> block) from HTML content.
        :return: HTML description
        """
        return html.unescape(self.html_soup.head.find('meta', attrs={"name": "description"})['content'])

    @mandatory_parsing_function
    def _extract_body(self) -> str:
        """
        Extract document body (not HTML body of course, if it is an article this will return
        only article body.
        :return: Document body
        """
        return ''

    @optional_parsing_function
    def _extract_doc_publication_time(self) -> datetime:
        """
        Extract document date and time (if present) of publication.
        :return: Document publication date and time as timestamp
        """
        try:
            time_text = self.html_soup.find('meta', attrs={'property': "article:published_time"}).get('content')
        except AttributeError:
            try:
                time_text = self.html_soup.find('time', attrs={'itemprop': 'datePublished'}).get('datetime')
            except AttributeError:
                time_text = self.html_soup.find('time').get('datetime')

        try:
            pub_time = datetime.strptime(time_text[:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError as err:
            raise DateFormatOptionalFailureException(err.args[0])
        return pub_time

    @optional_parsing_function
    def _extract_doc_update_time(self) -> Optional[datetime]:
        """
        Extract document date and time (if present) about when it was updated.
        :return: Document update date and time as timestamp
        """
        try:
            # TODO demander sur IRC si c'est le meilleur moyen de faire
            try:
                time_text = self.html_soup.find('meta', attrs={'property': "article:modified_time"}).get('content')
            except AttributeError:
                try:
                    time_text = self.html_soup.find('time', attrs={'itemprop': 'dateModified'}).get('datetime')
                except AttributeError:
                    time_text = self.html_soup.find_all('time')[1].get('datetime')
        except IndexError:
            # Should all fail, return None
            return None

        try:
            pub_time = datetime.strptime(time_text[:19], '%Y-%m-%dT%H:%M:%S')
        except ValueError as err:
            raise DateFormatOptionalFailureException(err.args[0])
        return pub_time

    @optional_parsing_function
    def _extract_href_sources(self) -> List[str]:
        """
        Extract sources displayed as links from the document.
        :return: list of sources contained in the document
        """
        return []

    @optional_parsing_function
    def _post_extract_href_sources(self, hrefs: List[str]) -> List[str]:
        """
        Change local links in fully qualified links, and discard local hash links.

        :param hrefs: Previously extracted hrefs
        :return:
        """
        result = []
        for href in hrefs:
            if re.match(r'^#', href):
                continue
            # Use first defined domain, should work "almost" every time
            try:
                url = get_truncated_url(re.sub(r'^/([^/])', self.domains[0] + r'/\1', href))
            except InvalidUrlException:
                continue
            result.append(url)

        return result

    @optional_parsing_function
    def _extract_category(self) -> str:
        """
        Extract category as given by the media (specialized media may have only one category).
        :return: the category of the document
        """
        return ''

    @optional_parsing_function
    def _extract_explicit_sources(self) -> List[str]:
        """
        Extract sources explicitly given in the document
        :return: list of explicit sources
        """
        return []

    @optional_parsing_function
    def _extract_keywords(self) -> List[str]:
        """
        Extract keywords displayed on the webpage
        :return: list of keywords
        """
        keywords_set = set()
        keywords_tags = self.html_soup.find_all('meta', attrs={'name': 'keywords'})
        if not keywords_tags:
            keywords_tags = self.html_soup.find_all('meta', attrs={'name': 'news_keywords'})
        for tag in keywords_tags:
            keywords = tag.get('content').split(',')
            keywords_set = keywords_set.union([word.strip() for word in keywords])
        return list(keywords_set)

    @staticmethod
    def _exclude_hrefs_by_attribute(html_as: List, attribute: str, value: str, parent=False):
        """
        Exclude local additional links (which are not really sources)
        :param html_as: As to be filtered
        :param attribute: Attribute of A which is targeted
        :param value: Value targeted
        :param parent: Test attribute and value on parent of A
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
    def _exclude_hrefs_by_regex(html_as: List, regex: str):
        reg = re.compile(regex)
        return [a for a in html_as if not reg.search(a['href'])]

    @staticmethod
    def _format_datetime(string: str, format_string: str) -> datetime:
        try:
            date = datetime.strptime(string, format_string)
        except ValueError as err:
            raise DateFormatOptionalFailureException from err
        return date
