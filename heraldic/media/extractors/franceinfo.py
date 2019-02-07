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

    test_urls = ['https://www.francetvinfo.fr/sports/foot/coupe-de-la-ligue-guingamp-decroche-son-billet-'
                 'pour-la-finale-en-battant-monaco-aux-tirs-au-but_3167035.html']

    def _extract_body(self):
        content_div = self.html_soup.select_one('#col-middle')

        alireaussi_tag = content_div.select_one('aside.a-lire-aussi')
        self._side_links = [tag.extract() for tag in alireaussi_tag.select('a')]

        [aside.decompose() for aside in content_div.find_all('aside')]
        content_div.select_one('div.content-feedback-block').decompose()
        return content_div

    def _extract_category(self):
        text = self.html_soup.select('nav.breadcrumb a')[-1].text
        # find('nav', attrs={'class': 'breadcrumb'}).find_all('a')[-1].text
        return text

    def _extract_news_agency(self):
        try:
            text = self.html_soup.select_one('span.author').text
        except AttributeError:
            return []
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return source.group(1)
        return ''
