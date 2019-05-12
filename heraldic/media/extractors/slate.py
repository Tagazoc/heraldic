#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
import json


class Slate(GenericMedia):
    """
    Class used for media "Slate".
    """
    supported_domains = ['www.slate.fr']
    id = 'slate'
    display_name = 'Slate'


class SlateExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "Slate".
    """
    test_urls = [
        'http://www.slate.fr/story/106623/sommeil-lever-avant-10h-torture-oxford-university'
    ]

    def _check_extraction(self):
        return True
        return self.html_soup.select_one('div.articleBody') is not None

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.field-item')
        side_links_tags = content_div.select('div.article_insert')
        self._side_links.extend([tag.extract().a for tag in side_links_tags])
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select_one('div.article-header__breadcrumb').a.text
        return text

    def _extract_keywords(self):
        for script in self.html_soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.text)
                return data['keywords']
            except KeyError:
                continue
        return []

    def _extract_side_links(self):
        side_links_tags = self.html_soup.select('div.feed-articles-aside')
        self._side_links.extend([tag.extract().a for tag in side_links_tags])
        return self._side_links
