#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BFM TV website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re


class BfmTv(GenericMedia):
    """
    Class used for extracting items from french media "BFM TV".
    """
    supported_domains = ['www.bfmtv.com']
    id = 'bfm_tv'
    display_name = 'BFM TV'

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'})

    def _extract_category(self):
        text = self.html_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[1].text
        return text

    def _extract_explicit_sources(self):
        text = self.html_soup.find('strong', attrs={'rel': 'author'}).text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return [source.group(1)]
        return []
