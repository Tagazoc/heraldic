#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Huffigton Post website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class HuffingtonPost(GenericMedia):
    """
    Class used for media "Huffington Post".
    """
    supported_domains = ['www.huffingtonpost.fr']
    id = 'huffington_post'
    articles_regex = [r'[0-9]{6}/?$']
    display_name = 'Huffington Post'


class HuffingtonPostExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "Huffington Post" in french langugage.
    """
    test_urls = ['https://www.huffingtonpost.fr/2019/02/06/la-rencontre-entre-luigi-di-maio-et-des-gilets-'
                 'jaunes-une-nouvelle-provocation-pour-paris_a_23663273/']
    default_extractor = True

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.post-contents')
        related_entries_tag = content_div.select_one('div.related-entries').extract()
        self._side_links = related_entries_tag.select('a')
        content_div.find(string=re.compile(r'à voir .*', re.IGNORECASE)).parent.parent.decompose()
        try:
            content_div.blockquote.decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/news/[^/]+/?$')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/tag/[^/]+/?$')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/[^/]+/?$')
        return html_as

    def _extract_category(self):
        span_text = self.html_soup.select_one('span.entry-eyebrow').text
        return span_text
