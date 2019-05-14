#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class RTL(GenericMedia):
    """
    Class used for media "".
    """
    supported_domains = ['www.rtl.fr']
    id = 'rtl'
    display_name = 'RTL'


class RTLExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "".
    """
    test_urls = ['https://www.rtl.fr/actu/debats-societe/glyphosate-ce-que-contient-vraiment-le-rapport-controverse-des-parlementaires-7797624741',
                 'https://www.rtl.fr/actu/justice-faits-divers/quimper-un-lyceen-decede-dans-son-etablissement-7797630147']

    def _check_extraction(self):
        return True

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.article-mask')
        related_tags = content_div.select('div.article-related')
        self._side_links.extend([tag.extract().a for tag in related_tags])
        try:
            recommandation_as = content_div.select_one('div.article-recommendation').extract().select('a')
            self._side_links.extend(recommandation_as)
        except AttributeError:
            pass
        try:
            content_div.select_one('span.read-more').extract()
        except AttributeError:
            pass
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select_one('div.article-follow').a.text
        return text

    def _extract_news_agency(self):
        return self.html_soup.select_one('span.article-social-author-position')

    def _extract_side_links(self):
        side_links_as = self.html_soup.select('div.linked-articles a')
        self._side_links.extend(side_links_as)
        return self._side_links
