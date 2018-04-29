#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'express website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function, mandatory_parsing_function
import re
from datetime import datetime


class LExpress(GenericMedia):
    """
    Class used for extracting items from french media "Le Monde".
    """
    domains = ['www.lexpress.fr', 'lexpansion.lexpress.fr']
    id = 'lexpress'
    display_name = 'L\'Express'

    @mandatory_parsing_function
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'article_container'}).text

    @optional_parsing_function
    def _extract_href_sources(self):
        html_as = self.html_soup.article.find('div', attrs={'class': 'article_container'}).find_all('a')
        return [a['href'] for a in html_as if a.get('href') is not None]

    @optional_parsing_function
    def _extract_category(self):
        html_category = self.html_soup.find('div', attrs={'class': 'article_category'}).find('a').text
        return html_category
