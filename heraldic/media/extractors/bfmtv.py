#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BFM TV website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class BfmTv(GenericMedia):
    """
    Class used for french media "BFM TV".
    """
    supported_domains = ['www.bfmtv.com']
    id = 'bfm_tv'
    articles_regex = [r'\.html$']
    display_name = 'BFM TV'


class BfmTvExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "BFM TV".
    """
    test_urls = ['https://www.bfmtv.com/politique/hulot-de-retour-en-forme-sur-la-scene-mediatique-apres-'
                 '3-mois-de-silence-1571892.html']

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'})

    def _extract_category(self):
        text = self.html_soup.select('ul.breadcrumb a')[1].text
        return text

    def _extract_news_agency(self):
        text = self.html_soup.find('strong', attrs={'rel': 'author'}).text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return source.group(1)
        return ''

    def _extract_side_links(self):
        return self.html_soup.select('ul.related-article a')
