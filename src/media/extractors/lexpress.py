#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'express website extractor implementation.
"""

from src.media.generic_media import GenericMedia, handle_parsing_errors
import re
from datetime import datetime


class LExpress(GenericMedia):
    """
    Class used for extracting items from french media "Le Monde".
    """
    domains = ['www.lexpress.fr', 'lexpansion.lexpress.fr']
    id = 'lexpress'
    display_name = 'L\'Express'

    @handle_parsing_errors
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'article_container'}).text

    @handle_parsing_errors
    def _extract_doc_publication_time(self):
        time_text = self.html_soup.find('time', attrs={'itemprop': 'datePublished'}).get('datetime')
        return datetime.strptime(time_text[:-6], '%Y-%m-%dT%H:%M:%S')

    @handle_parsing_errors
    def _extract_doc_update_time(self):
        try:
            time_text = self.html_soup.find('time', attrs={'itemprop': 'dateModified'}).get('datetime')
            return datetime.strptime(time_text[:-6], '%Y-%m-%dT%H:%M:%S')
        except AttributeError:
            return None

    @handle_parsing_errors
    def _extract_href_sources(self):
        html_as = self.html_soup.article.find('div', attrs={'class': 'article_container'}).find_all('a')
        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_category(self):
        html_category = self.html_soup.find('div', attrs={'class': 'article_category'}).find('a').text
        return html_category
