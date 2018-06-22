#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Europe 1 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re


class Europe1(GenericMedia):
    """
    Class used for extracting items from french media "Europe 1".
    """
    supported_domains = ['www.europe1.fr']
    id = 'europe_1'
    display_name = 'Europe 1'

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'})

    def _extract_category(self):
        text = self.html_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('span')[-1].text
        return text

    def _extract_news_agency(self):
        text = self.html_soup.find('div', attrs={'class': 'author'}).find('div', attrs={'class': 'titre'}).text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return [source.group(1)]
        return []
