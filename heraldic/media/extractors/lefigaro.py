#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Figaro website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class LeFigaro(GenericMedia):
    """
    Class used for french media "Le Figaro".
    """
    supported_domains = ['www.lefigaro.fr']
    id = 'le_figaro'
    display_name = 'Le Figaro'


class LeFigaroExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Figaro".
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'class': 'fig-content__body'}).extract()
        bs = content_div.find_all('b')
        [b.decompose() for b in bs if re.search(r'LIRE AUSSI', b.text, re.IGNORECASE)]
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'author', parent=True)

        return html_as

    def _extract_category(self):
        html_li = self.html_soup.find('li', attrs={'class': 'fig-breadcrumb__item--current'})
        span_text = html_li.find('span').text
        return span_text

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'class': 'fig-premium-paywall'}) is not None
