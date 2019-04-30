#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Europe 1 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class Europe1(GenericMedia):
    """
    Class used for french media "Europe 1".
    """
    supported_domains = ['www.europe1.fr']
    id = 'europe_1'
    articles_regex = [r'[0-9]{6}$']
    display_name = 'Europe 1'


class Europe1Extractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Europe 1".
    """

    test_urls = ['https://www.europe1.fr/societe/enlysee-la-nouvelle-boutique-en-ligne-qui-parodie-les'
                 '-produits-de-lelysee-3762425',
                 'https://www.europe1.fr/politique/la-cote-de-macron-remonte-de-6-points-a-34-3852422']

    def _extract_body(self):
        return self.html_soup.select_one('article section.content')

    def _extract_category(self):
        text = self.html_soup.select('ul.breadcrumb span')[-1].text
        return text

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/dossiers/')
        return html_as

    def _extract_news_agency(self):
        return self.html_soup.select_one('div.author div.titre')

    def _extract_side_links(self):
        return self.html_soup.select('footer.footer-article div.memetheme a')
