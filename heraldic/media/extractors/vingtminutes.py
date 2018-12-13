#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
20 minutes website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy


class VingtMinutes(GenericMedia):
    """
    Class used for french media "20 Minutes".
    """
    supported_domains = ['www.20minutes.fr']
    id = '20minutes'
    display_name = '20 Minutes'


class VingtMinutesExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "20 Minutes".
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).article.find('div', attrs={'class': 'content'}).extract()
        try:
            content_div.find('div', attrs={'class': 'tags'}).decompose()
        except AttributeError:
            pass
        try:
            content_div.find('div', attrs={'class': 'sharebar'}).decompose()
        except AttributeError:
            pass
        [lire_aussi.decompose() for lire_aussi in content_div.find_all('a', attrs={'class': 'highlight'})]
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        # Also exclude internal links for groups of articles
        html_as = self._exclude_hrefs_by_regex(html_as, r'/dossier/')

        # And "generic" links, which seem to be used within one or two separators :
        html_as = self._exclude_hrefs_by_regex(html_as, r'/(?:[^/]+/)?[^/]+/?$')

        return html_as

    def _extract_category(self):
        html_category = self.html_soup.find('span', attrs={'class': 'teaser-headline'}).text
        return html_category
