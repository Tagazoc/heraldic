#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fdesouche website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class Fdesouche(GenericMedia):
    """
    Class used for french media "fdesouche".
    """
    supported_domains = ['www.fdesouche.com']
    id = 'fdesouche'
    articles_regex = [r'/[0-9]{6}']
    display_name = 'Fdesouche'


class FdesoucheExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "fdesouche".
    """
    test_urls = ['http://www.fdesouche.com/1153419-emmanuel-macron-nous-sommes-dans-un-monde-de-migrations'
                 '-je-ne-crois-pas-du-tout-aux-gens-qui-font-des-murs-ca-ne-marche-pas']

    def _extract_title(self):
        title = super(FdesoucheExtractor, self)._extract_title()
        return re.sub(r' - Fdesouche$', '', title)

    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'id': 'content-area'})

        try:
            content_div.select_one('div.post-image').decompose()
        except AttributeError:
            pass
        try:
            post_navigation = content_div.select_one('div.wp-post-navigation').extract()
            self._side_links.extend(post_navigation.select('a'))
        except AttributeError:
            pass
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_iframes = self._body_tag.find_all('iframe')

        return html_as + html_iframes

    def _extract_category(self):
        text = self.html_soup.find('div', attrs={'id': 'crumbs'}).find_all('a')[1].text
        return text

    def _extract_news_agency(self):
        return ''
