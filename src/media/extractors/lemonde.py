#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.generic_media import GenericMedia
import re
from datetime import datetime


class LeMonde(GenericMedia):
    """
    Class used for extracting items from french media "Le Monde".
    """
    domains = ['www.lemonde.fr']
    id = 'le_monde'
    display_name = 'Le Monde'

    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'id': 'articleBody'})

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'lien_interne')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'lire', parent=True)
        return html_as

    def _extract_category(self):
        html_title = self.html_soup.find('div', attrs={'class': 'tt_rubrique_ombrelle'}).contents[1].text
        return html_title

    def _extract_explicit_sources(self):
        html_span = self.html_soup.find('span', attrs={'id': 'publisher'})
        data_source = html_span['data-source']
        source = re.search(r' avec (.*)', data_source)
        try:
            sources = source.group(1)
        except AttributeError:
            return []
        sources = sources.split(' et ')
        return sources

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'class': 'teaser_article'}) is not None
