#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
France Inter website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class FranceInter(GenericMedia):
    """
    Class used for media "France Inter".
    """
    supported_domains = ['www.franceinter.fr']
    id = 'france_inter'
    display_name = 'France Inter'


class FranceInterExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "France Inter".
    """
    test_urls = ['https://www.franceinter.fr/politique/les-marcheurs-ont-ils-modifie-les-regles-du-csa-a-leur-avantage']

    def _check_extraction(self):
        return True
        return self.html_soup.select_one('div.articleBody') is not None

    def _extract_body(self):
        return self.html_soup.select_one('article.content-body')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select('ul.breadcrumb-list li a span')[1].text
        return text

    def _extract_side_links(self):
        side_links_as = self.html_soup.select('div.recommendations a')
        self._side_links.extend(side_links_as)
        return self._side_links
