#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mr Mondialisation website extractor implementation.
"""

from src.media.generic_media import GenericMedia, handle_parsing_errors
import re
from datetime import datetime
from copy import copy


class MrMondialisation(GenericMedia):
    """
    Class used for extracting items from french media "20 Minutes".
    """
    domains = ['mrmondialisation.org']
    id = 'MrMondialisation'
    display_name = 'Mr Mondialisation'

    @handle_parsing_errors
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'td-post-content'}).text

    @handle_parsing_errors
    def _extract_href_sources(self):
        html_as = self.html_soup.article.find('div', attrs={'class': 'td-post-content'}).find_all('a')
        return [a['href'] for a in html_as if a.get('href') is not None]

    @handle_parsing_errors
    def _extract_category(self):
        html_category = self.html_soup.find_all('a', attrs={'class': 'entry-crumb'})[-1].span.text
        return html_category
