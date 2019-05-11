#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class MediaName(GenericMedia):
    """
    Class used for media "".
    """
    supported_domains = ['']
    id = ''
    display_name = ''


class MediaNameExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "".
    """
    test_urls = []

    def _check_extraction(self):
        return self.html_soup.select_one('div.articleBody') is not None

    def _extract_body(self):
        return self.html_soup.select_one('div.articleBody')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select('ul.breadcrumb').find_all('a')[1].text
        return text

    def _extract_news_agency(self):
        return self.html_soup.find('strong', attrs={'rel': 'author'})
