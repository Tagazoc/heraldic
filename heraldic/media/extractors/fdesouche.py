#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fdesouche website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy


class Fdesouche(GenericMedia):
    """
    Class used for french media "fdesouche".
    """
    supported_domains = ['www.fdesouche.com']
    id = 'fdesouche'
    display_name = 'Fdesouche'


class FdesoucheExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "fdesouche".
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'id': 'content-area'})

        try:
            content_div.find('div', attrs={'class': 'post-image'}).decompose()
        except AttributeError:
            pass
        try:
            content_div.find('div', attrs={'class': 'wp-post-navigation'}).decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_iframes = self._body_tag.find_all('iframe')

        return html_as + html_iframes

    def _extract_category(self):
        text = self.html_soup.find('div', attrs={'id': 'crumbs'}).find_all('a')[1].text
        return text

    def _extract_news_agency(self):
        return ''
