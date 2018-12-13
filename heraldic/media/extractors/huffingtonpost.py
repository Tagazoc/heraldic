#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Huffigton Post website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy


class HuffingtonPost(GenericMedia):
    """
    Class used for media "Huffington Post".
    """
    supported_domains = ['www.huffingtonpost.fr']
    id = 'huffington_post'
    display_name = 'Huffington Post'


class HuffingtonPostExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "Huffington Post" in french langugage.
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'class': 'post-contents'})
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
        span_text = self.html_soup.find('span', attrs={'class': 'entry-eyebrow'}).text
        return span_text
