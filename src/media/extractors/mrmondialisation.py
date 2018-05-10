#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mr Mondialisation website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function
import re
from datetime import datetime
from copy import copy


class MrMondialisation(GenericMedia):
    """
    Class used for extracting items from french media "Mr Mondialisation".
    """
    domains = ['mrmondialisation.org']
    id = 'MrMondialisation'
    display_name = 'Mr Mondialisation'

    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'td-post-content'})

    def _extract_category(self):
        html_category = self.html_soup.find_all('a', attrs={'class': 'entry-crumb'})[-1].span.text
        return html_category
