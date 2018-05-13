#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Parisien's website extractor implementation.
"""

from src.media.generic_media import GenericMedia
import re


class MediaName(GenericMedia):
    """
    Class used for extracting items from french media "Le Parisien".
    """
    domains = ['www.leparisien.fr']
    id = 'le_parisien'
    display_name = 'Le Parisien'

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'article-full__body-content'})

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('span', attrs={'class': 'article-full__breadcrumb'}).find_all('span')[-1].text
        return text

    def _extract_explicit_sources(self):
        try:
            text = self.html_soup.find('span', attrs={'class': 'article-full__author-label'}).text
        except AttributeError:
            return []
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return [source.group(1)]
        return []
