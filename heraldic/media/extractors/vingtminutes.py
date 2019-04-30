#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
20 minutes website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class VingtMinutes(GenericMedia):
    """
    Class used for french media "20 Minutes".
    """
    supported_domains = ['www.20minutes.fr']
    id = '20minutes'
    articles_regex = [r'/[0-9]+-[0-9]+']
    display_name = '20 Minutes'


class VingtMinutesExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "20 Minutes".
    """
    test_urls = ['https://www.20minutes.fr/societe/2454163-20190218-parcoursup-dossiers-candidats'
                 '-anonymises-lycee-origine-restera']

    def _extract_body(self):
        content_div = self.html_soup.article.select_one('div.content').extract()
        try:
            content_div.select_one('.tags').decompose()
        except AttributeError:
            pass
        try:
            content_div.select_one('.sharebar').decompose()
        except AttributeError:
            pass
        side_links = [lire_aussi.extract().select('a') for lire_aussi in content_div.select('a.highlight')]
        self._side_links.extend([a for side_link_a in side_links for a in side_link_a])
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.select('a')

        # Also exclude internal links for groups of articles
        html_as = self._exclude_hrefs_by_regex(html_as, r'/dossier/')

        # And "generic" links, which seem to be used within one or two separators :
        html_as = self._exclude_hrefs_by_regex(html_as, r'/(?:[^/]+/)?[^/]+/?$')

        return html_as

    def _extract_category(self):
        html_category = self.html_soup.select_one('span.teaser-headline').text
        return html_category

    def _extract_news_agency(self):
        return self.html_soup.select_one('p.authorsign-label')

    def _extract_side_links(self):
        self._side_links.extend(self.html_soup.select('block-contentLinks a'))
        return self._side_links
