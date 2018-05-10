#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing generic DocumentExtractor class.
"""

from typing import List, Optional
import html
from src.models.document_model import DocumentModel
from bs4 import BeautifulSoup
from bs4.element import Tag
from src.store import index_searcher
from datetime import datetime
import src.misc.exceptions as ex
from src.misc.functions import get_truncated_url
import re


def optional_parsing_function(decorated):
    def wrapper(self, *args):
        try:
            result = decorated(self, *args)
        except Exception as err:
            raise ex.HTMLParsingException from err
        return result

    return wrapper


def mandatory_parsing_function(decorated):
    def wrapper(self, *args):
        try:
            result = decorated(self, *args)
        except Exception as err:
            raise ex.MandatoryParsingException from err
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
    unwanted_extensions = ['jpg', 'png', 'gif']

    def __init__(self, dm: DocumentModel) -> None:
        """
        Initialize extractor by parsing HTML contained in document model.

        :param dm: Document model which will contain all extracted items.
        """
        self.html_soup = BeautifulSoup(dm.content.render_for_display(), "html.parser")
        self.dm = dm
        self._body_tag = None
        """ Body backup, wich can be reused for other attributes. """

    @classmethod
    def get_document_count(cls) -> int:
        return index_searcher.count(q='media:' + cls.id)

    def extract_fields(self, debug=False):
        """
        This function calls every extraction function supported by the media.
        """
        mandatory_k = [k for k, v in self.dm.attributes.items() if v.mandatory]
        optional_k = [k for k in self.dm.attributes.keys() if k not in mandatory_k]

        # First process mandatory attributes, then optionals
        for k in mandatory_k + optional_k:
            v = self.dm.attributes[k]
            if v.extractible:
                try:
                    # "Extract" function returns an HTML tag, a list of tags, or text
                    func = getattr(self, "_extract_" + k)
                    extracted_data = func()
                    try:
                        # Optional post-treatment may apply changes to data before returning it
                        post_func = getattr(self, "_post_extract_" + k)
                    except AttributeError:
                        pass
                    else:
                        extracted_data = post_func(extracted_data)
                    v.set_from_extraction(extracted_data)
                except Exception as err:
                    if v.mandatory:
                        raise ex.MandatoryParsingException(k, self.dm.urls.value[0], err)
                    else:
                        # Handle raised exception immediately to log
                        try:
                            raise ex.OptionalParsingException(k, self.dm.urls.value[0], err)
                        except ex.OptionalParsingException as parsing_exc:
                            v.parsing_error = parsing_exc.message
                            if debug:
                                raise

    def _extract_media(self) -> str:
        """
        Function which returns media name attribute, in order to work with extract_fields function.
        :return: Media name
        """
        return self.id

    def _extract_title(self) -> str:
        """
        Extract HTML title (in <head> block) from HTML content.
        :return: HTML title
        """
        return html.unescape(self.html_soup.head.title.text)

    def _extract_description(self) -> str:
        """
        Extract description (in meta tag, in <head> block) from HTML content.
        :return: HTML description
        """
        return html.unescape(self.html_soup.head.find('meta', attrs={"name": "description"})['content'])

    def _extract_body(self) -> Tag:
        """
        Extract document body (not HTML body of course, if it is an article this will return
        only article body.
        :return: Document body
        """
        raise NotImplementedError

    def _post_extract_body(self, body: Tag) -> str:
        """
        Remove unwanted tags in body, such as scripts.
        :param body:
        :return:
        """

        self._body_tag = body
        return body.text

    def _extract_doc_publication_time(self) -> str:
        """
        Extract document date and time (if present) of publication.
        :return: Document publication date and time as timestamp
        """
        try:
            time_text = self.html_soup.find('meta', attrs={'property': "article:published_time"}).get('content')
        except AttributeError:
            time_text = self.html_soup.find('time', attrs={'itemprop': 'datePublished'}).get('datetime')

        return time_text

    def _post_extract_doc_publication_time(self, text: str) -> datetime:
        return self._format_time(text, 'doc_publication_time')

    def _extract_doc_update_time(self) -> Optional[str]:
        """
        Extract document date and time (if present) about when it was updated.
        :return: Document update date and time as timestamp
        """
        try:
            # TODO demander sur IRC si c'est le meilleur moyen de faire
            try:
                time_text = self.html_soup.find('meta', attrs={'property': "article:modified_time"}).get('content')
            except AttributeError:
                time_text = self.html_soup.find('time', attrs={'itemprop': 'dateModified'}).get('datetime')
        except AttributeError:
            # Should all fail, return None
            return None
        return time_text

    def _post_extract_doc_update_time(self, text: str) -> Optional[datetime]:
        if text is None:
            return None
        return self._format_time(text, 'doc_update_time')

    def _extract_href_sources(self) -> List[Tag]:
        """
        Extract sources displayed as links from the document.
        :return: list of sources contained in the document
        """
        return self._body_tag.find_all('a')

    def _post_extract_href_sources(self, a_tags: List[Tag]) -> List[str]:
        """
        Change local links in fully qualified links, and discard local hash links, and unwanted extensions such as
        images.

        :param a_tags: Previously extracted <a> tags
        :return:
        """
        hrefs = [a['href'] for a in a_tags if a.get('href') is not None]
        result = []
        extension_pattern = re.compile(r'(?:' + r'|'.join(self.unwanted_extensions) + r')(?:\?|#|$)', re.IGNORECASE)
        for href in hrefs:
            if re.match(r'^#', href):
                continue
            if extension_pattern.search(href):
                continue
            # Use first defined domain, should work "almost" every time
            try:
                url = get_truncated_url(re.sub(r'^/([^/])', self.domains[0] + r'/\1', href))
            except ex.InvalidUrlException:
                continue
            result.append(url)

        return result

    def _extract_category(self) -> str:
        """
        Extract category as given by the media (specialized media may have only one category).
        :return: the category of the document
        """
        return ''

    def _extract_explicit_sources(self) -> List[str]:
        """
        Extract sources explicitly given in the document
        :return: list of explicit sources
        """
        return []

    def _extract_keywords(self) -> List[str]:
        """
        Extract keywords displayed on the webpage
        :return: list of keywords
        """
        keywords_set = set()
        keywords_tags = self.html_soup.find_all('meta', attrs={'name': 'keywords'})
        if not keywords_tags:
            keywords_tags = self.html_soup.find_all('meta', attrs={'name': 'news_keywords'})
        if not keywords_tags:
            keywords_tags = self.html_soup.find_all('meta', attrs={'property': 'keywords'})
        for tag in keywords_tags:
            keywords = tag.get('content').split(',')
            keywords_set = keywords_set.union([word.strip() for word in keywords])
        return list(keywords_set)

    def _extract_subscribers_only(self) -> bool:
        """
        Extract whether document is reserved to subscribers.
        :return: Default it is readable by anyone.
        """
        return False

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

    def _format_time(self, text: str, attribute_name: str) -> datetime:
        match = re.match(r'(\d{4}-\d{2}-\d{2})(?:CES)?T(\d{2}:\d{2})((?::\d{2})?)', text[:19])
        try:
            seconds = match.group(3) if len(match.group(3)) > 0 else ':00'

            time_text = match.group(1) + 'T' + match.group(2) + seconds
        except ValueError as err:
            raise ex.DateFormatParsingException(attribute_name, self.dm.urls.value[0], err)
        time = datetime.strptime(time_text, '%Y-%m-%dT%H:%M:%S')
        return time
