#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Huffigton Post website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function, mandatory_parsing_function


class HuffingtonPost(GenericMedia):
    """
    Class used for extracting items from french media "Huffington Post".
    """
    domains = ['www.huffingtonpost.fr']
    id = 'huffington_post'
    display_name = 'Huffington Post'

    @mandatory_parsing_function
    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'post-contents'}).text

    @optional_parsing_function
    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'post-contents'}).find_all('a')
        exclude_as = self.html_soup.find('div', attrs={'class': 'post-contents'}).blockquote.find_all('a')
        html_as = [a for a in html_as if a not in exclude_as]

        return [a['href'] for a in html_as if a.get('href') is not None]

    @optional_parsing_function
    def _extract_category(self):
        span_text = self.html_soup.find('span', attrs={'class': 'entry-eyebrow'}).text
        return span_text
