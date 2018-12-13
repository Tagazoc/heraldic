#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"L'Humanité" website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor


class LHumanite(GenericMedia):
    """
    Class used for french media "L'Humanité".
    """
    supported_domains = ['www.humanite.fr']
    id = 'l_humanite'
    display_name = 'L\'Humanité'


class LHumaniteExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "L'Humanité".
    """
    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'field-name-field-news-text'})

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('div', attrs={'id': 'block-system-main-menu'}).\
            find('ul', attrs={'class': 'menu'}).find('a', attrs={'class': 'active'}).text
        return text

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'id': 'non-abonnes-link-url'}) is not None
