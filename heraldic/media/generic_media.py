#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing generic DocumentExtractor class.
"""

from typing import List, Optional
import html
import inspect
import sys
from heraldic.models.document_model import DocumentModel
from bs4 import BeautifulSoup
from bs4.element import Tag
from heraldic.store import index_searcher
from datetime import datetime
import heraldic.misc.exceptions as ex
from heraldic.misc.functions import get_truncated_url, get_domain, get_resource
from copy import copy
import json
import re


class GenericMedia(object):
    """
        Generic class for a media, should not be directly instanciated.
    """
    supported_domains = ['www.heraldic-project.org', 'hrldc.org']
    """The domains used in URLs of the selected media"""

    articles_regex = [r'.*']

    """A list of regexes which help recognizing whether an URL is an article or not"""

    id = 'generic'
    display_name = 'Generic'

    @classmethod
    def get_extractors(cls) -> List:
        return [v for k, v in inspect.getmembers(sys.modules[cls.__module__], inspect.isclass)
                if k != 'GenericMediaExtractor'and issubclass(v, GenericMediaExtractor)]

    @classmethod
    def is_url_article(cls, url):
        """
        Check whether an URL may be associated with an article, based on its format.
        :param url: The URL to be tested
        """
        return any([regex.search(url) for regex in cls._articles_compiled_regex()])

    @classmethod
    def _articles_compiled_regex(cls):
        return [re.compile(regex) for regex in cls.articles_regex]

    @classmethod
    def topmost_domains(cls):
        return [re.match(r'(?:.*\.)?([^.]+\.[^.]+)', domain).group(1) for domain in cls.supported_domains]

    @classmethod
    def get_document_count(cls, unit: str=None, count: int=None) -> int:

        units_map = {
            'days': 'd',
            'hours': 'h',
            'months': 'M'
        }
        if unit:
            elastic_unit = units_map[unit]
            query = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'term': {
                                    'media': cls.id
                                }
                            },
                            {
                                'range': {
                                    'doc_publication_time': {
                                        'gt': 'now-' + str(count + 1) + elastic_unit,
                                        'lte': 'now-' + str(count) + elastic_unit
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        else:
            query = {
                'query': {
                    'term': {
                        'media': cls.id
                    }
                }
            }
        return index_searcher.count(body_query=query)

    @classmethod
    def get_data(cls):
        return {
            'id': cls.id,
            'name': cls.display_name,
            'count': cls.get_document_count()
        }

    @classmethod
    def get_counts(cls, unit, number):
        counts = [cls.get_document_count(unit, i) for i in range(number)]
        return {
            'id': cls.id,
            'name': cls.display_name,
            'counts': counts
        }



class GenericMediaExtractor(object):
    """
        Generic class for attribute extraction from a document, should not be directly instanciated.
    """
    unwanted_extensions = ['jpg', 'png', 'gif']
    parser = 'html.parser'
    _supported_domains = []
    default_extractor = True
    test_url = ''

    def __init__(self, dm: DocumentModel) -> None:
        """
        Initialize extractor by parsing HTML contained in document model.

        :param dm: Document model which will contain all extracted items.
        """
        content = dm.content.render_for_display()
        self.html_soup = BeautifulSoup(content, self.parser)
        self.dm = dm

        self._side_links = []
        """ This list is used for extraction of 'side_links' attribute, which help to harvest plenty of articles 
        without being real sources for an article. It is usually extracted in extract_href_sources function. """

        self._body_tag = None
        """ Body backup, which can be reused for other attributes. """

        self._document_type = 'article'
        """ Document type : article, video, panorama... """

    @property
    def _media_class(self):
        return [v for k, v in inspect.getmembers(sys.modules[self.__module__], inspect.isclass)
                if k != 'GenericMedia' and issubclass(v, GenericMedia)][0]

    @property
    def supported_domains(self):
        if self._supported_domains:
            return self._supported_domains
        return self._media_class.supported_domains

    def check_extraction(self) -> bool:
        """

        :return:
        """
        try:
            return self._check_extraction()
        except Exception:
            return False

    def _check_extraction(self) -> bool:
        return True

    def extract_fields(self, raise_on_optional=False):
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
                        # Handle raised exception immediately set parsing error to attribute, but raise it
                        try:
                            raise ex.MandatoryParsingException(k, self.dm.urls.value[0], err)
                        except ex.MandatoryParsingException as parsing_exc:
                            v.parsing_error = parsing_exc.message
                            raise
                    else:
                        # Handle raised exception immediately to log
                        try:
                            raise ex.OptionalParsingException(k, self.dm.urls.value[0], err)
                        except ex.OptionalParsingException as parsing_exc:
                            v.parsing_error = parsing_exc.message
                            if raise_on_optional:
                                raise

    def _extract_media(self) -> str:
        """
        Function which returns media name attribute, in order to work with extract_fields function.
        :return: Media name
        """
        return self._media_class().id

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
        # Copy body tag to avoid affecting global soup
        body = copy(body)
        [tag.decompose() for tag in body.find_all('script')]
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
            try:
                time_text = self.html_soup.find('time', attrs={'itemprop': 'datePublished'}).get('datetime')
            except AttributeError:
                try:
                    time_text = self.html_soup.find('time').get('datetime')
                except AttributeError:
                    time_text = self.html_soup.find('meta', attrs={'property': "og:article:published_time"}).get('content')

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
                try:
                    time_text = self.html_soup.find('time', attrs={'itemprop': 'dateModified'}).get('datetime')
                except AttributeError:
                    try:
                        time_text = self.html_soup.find_all('time')[1].get('datetime')
                    except AttributeError:
                        time_text = self.html_soup.find('meta', attrs={'property': "og:article:modified_time"}).get(
                            'content')
        except IndexError:
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

    def _post_extract_href_sources(self, source_tags: List[Tag]) -> List[str]:
        """
        Change local links in fully qualified links, and discard local hash links, and unwanted extensions such as
        images.

        :param source_tags: Previously extracted <a> tags
        :return:
        """
        hrefs = [a['href'] for a in source_tags if a.get('href') is not None]
        iframe_hrefs = [iframe['src'] for iframe in source_tags if iframe.get('src') is not None]
        result = []
        extension_pattern = re.compile(r'(?:' + r'|'.join(self.unwanted_extensions) + r')(?:\?|#|$)', re.IGNORECASE)
        for href in hrefs + iframe_hrefs:
            if re.match(r'^#', href):
                continue
            if extension_pattern.search(href):
                continue
            # Use first defined domain, should work "almost" every time
            try:
                protocol, url = get_truncated_url(re.sub(r'^/([^/])', self.supported_domains[0] + r'/\1', href))
            except ex.InvalidUrlException:
                continue
            # We let (for now) protocol in those URLS
            result.append(protocol + url)

        # Only keep distinct values
        result = list(set(result))
        return result

    def _extract_category(self) -> str:
        """
        Extract category as given by the media (specialized media may have only one category).
        :return: the category of the document
        """
        return ''

    def _extract_news_agency(self) -> str:
        """
        Extract news agency explicitly given in the document
        :return: news agency name
        """
        return ''

    def _extract_explicit_sources(self) -> List[str]:
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
        if not keywords_tags:
            try:
                data = json.loads(self.html_soup.find('script', type='application/ld+json').text)
                keywords = data['keywords']
                if isinstance(keywords, str):
                    keywords = keywords.split(',')
                    keywords = [word.strip() for word in keywords]
                return keywords
            except AttributeError:
                pass
            except KeyError:
                pass
        return list(keywords_set)

    def _extract_document_type(self) -> str:
        """
        "Extract" document type : article, video, panorama. Actually, this attribute is defined in body extraction and
        placed in "_document_type" attribute.
        :return:
        """
        return self._document_type

    def _extract_subscribers_only(self) -> bool:
        """
        Extract whether document is reserved to subscribers.
        :return: Default it is readable by anyone.
        """
        return False

    def _extract_side_links(self) -> List[str]:
        """
        Use _side_links attribute, which is usually extracted in href_sources attribute, and compare its content with
        URL format used for articles on the media website
        :return:
        """
        return [url for url in self._side_links if self._media_class().is_url_article(url)]

    def _exclude_hrefs(self, html_as: List, side_links=True, attribute_name: str='', attribute_value: str='',
                       is_parent_attribute=False, tags: List[str]=None, regex: str='', only_internal_links=False):
        """
        Exclude local additional links (which are not really sources)
        :param html_as: As to be filtered
        :param attribute_name: Attribute of A which is targeted
        :param attribute_value: Value targeted
        :param is_parent_attribute: Test attribute and value on parent of A
        :return:
        """
        removed_as = []
        reg = re.compile(regex) if regex else None

        for a in html_as:
            if attribute_name:
                try:
                    tag = a
                    if is_parent_attribute:
                        tag = a.parent
                    if attribute_value in tag[attribute_name]:
                        removed_as.append(a)
                        html_as.remove(a)
                except KeyError:
                    # No such attribute for <a> tag
                    pass
            if tags is not None:
                tag = a.parent
                if tag.name in tags:
                    removed_as.append(a)
                    html_as.remove(a)
            if only_internal_links and not self._is_internal_link(a['href']):
                removed_as.append(a)
                html_as.remove(a)
            if regex:
                # If we only want internal links, throw away external ones

                if not reg.match(a['href']):
                    try:
                        if reg.match(get_resource(a['href'])):
                            removed_as.append(a)
                            html_as.remove(a)
                    except ex.InvalidUrlException:
                        removed_as.append(a)
                        html_as.remove(a)

        if side_links:
            self._side_links.extend(removed_as)

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
    def _exclude_hrefs_by_parent_tag(html_as: List, tags: List[str]):
        """
        Exclude local additional links (which are not really sources) from their parent tag.
        :param html_as: As to be filtered
        :return:
        """
        filtered_as = []
        for a in html_as:
            tag = a.parent
            if tag.name in tags:
                continue
            filtered_as.append(a)

        return filtered_as

    # TODO invalidurl qui ne print pas
    @classmethod
    def _exclude_hrefs_by_regex(cls, html_as: List, regex: str, only_internal_links=True):
        reg = re.compile(regex)
        filtered_as = []
        for a in html_as:
            if only_internal_links and not cls._is_internal_link(a['href']):
                continue
            if not reg.match(a['href']):
                try:
                    if not reg.match(get_resource(a['href'])):
                        filtered_as.append(a)
                except ex.InvalidUrlException:
                    filtered_as.append(a)

        return filtered_as

    @classmethod
    def _is_internal_link(cls, url):
        # Local links
        if re.match(r'/', url):
            return True
        try:
            if get_domain(url) in cls.supported_domains:
                return True
            else:
                return False
        except ex.InvalidUrlException:
            return False

    def _format_time(self, text: str, attribute_name: str) -> datetime:
        match = re.match(r'(\d{4}-\d{2}-\d{2})(?:CES)?T(\d{2}:\d{2})((?::\d{2})?)', text[:19])
        try:
            seconds = match.group(3) if len(match.group(3)) > 0 else ':00'

            time_text = match.group(1) + 'T' + match.group(2) + seconds
        except ValueError as err:
            raise ex.DateFormatParsingException(attribute_name, self.dm.urls.value[0], err)
        time = datetime.strptime(time_text, '%Y-%m-%dT%H:%M:%S')
        return time
