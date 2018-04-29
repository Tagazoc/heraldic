#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BFM TV website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function, mandatory_parsing_function
import re


class BfmTv(GenericMedia):
    """
    Class used for extracting items from french media "Huffington Post".
    """
    domains = ['www.bfmtv.com']
    id = 'bfm_tv'
    display_name = 'BFM TV'

    @mandatory_parsing_function
    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'}).text

    @optional_parsing_function
    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'itemprop': 'articleBody'}).find_all('a')

        return [a['href'] for a in html_as if a.get('href') is not None]

    @optional_parsing_function
    def _extract_category(self):
        text = self.html_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[1].text
        return text

    @optional_parsing_function
    def _extract_explicit_sources(self):
        text = self.html_soup.find('strong', attrs={'rel': 'author'}).text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return [source.group(1)]
        return []
