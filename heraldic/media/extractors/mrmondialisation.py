#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mr Mondialisation website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor


class MrMondialisation(GenericMedia):
    """
    Class used for french media "Mr Mondialisation".
    """
    supported_domains = ['mrmondialisation.org']
    id = 'MrMondialisation'
    articles_regex = [r'/[a-z-0-9]+$']
    display_name = 'Mr Mondialisation'


class MrMondialisationExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Mr Mondialisation".
    """
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'td-post-content'})

    def _extract_category(self):
        html_category = self.html_soup.find_all('a', attrs={'class': 'entry-crumb'})[-1].span.text
        return html_category
