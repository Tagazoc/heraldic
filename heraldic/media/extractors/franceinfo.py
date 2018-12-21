#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
France Info website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
from copy import copy


class FranceInfo(GenericMedia):
    """
    Class used for french media "France Info".
    """
    supported_domains = ['www.francetvinfo.fr']
    id = 'france_info'
    articles_regex = [r'\.html$']
    display_name = 'France Info'


class FranceInfoExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "France Info".
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'id': 'col-middle'})
        [aside.decompose() for aside in content_div.find_all('aside')]
        return content_div

    def _extract_category(self):
        text = self.html_soup.find('nav', attrs={'class': 'breadcrumb'}).find_all('a')[-1].text
        return text

    def _extract_news_agency(self):
        try:
            text = self.html_soup.find('span', attrs={'class': 'author'}).text
        except AttributeError:
            return []
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return source.group(1)
        return ''
