#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.generic_media_extractor import GenericMediaExtractor
import re


class LiberationExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Libération".
    """
    domains = ['www.liberation.fr']
    media_name = 'liberation'

    def _extract_document_body(self):
        return self.html_soup.find('div', attrs={'class': 'article-body'}).text

    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'article-body'}).find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'author', parent=True)

        return [a['href'] for a in html_as]

    def _extract_category(self):
        category = self.html_soup.find('div', attrs={'class': 'article-subhead'}).text
        return category

    def _extract_explicit_sources(self):
        a_text = self.html_soup.find('span', attrs={'class': 'author'}).a.text
        source = re.search(r', avec (.*)', a_text)
        return [source.group(1)]
