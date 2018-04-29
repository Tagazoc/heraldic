#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function, mandatory_parsing_function
import re
from src.misc.exceptions import HTMLOptionalParsingFailureException


class Liberation(GenericMedia):
    """
    Class used for extracting items from french media "Libération".
    """
    domains = ['www.liberation.fr']
    id = 'liberation'
    display_name = 'Libération'

    @mandatory_parsing_function
    def _extract_body(self):
        try:
            body = self.html_soup.find('div', attrs={'class': 'article-body'}).text
        except AttributeError as err:
            raise HTMLOptionalParsingFailureException from err
        return body

    @optional_parsing_function
    def _extract_title(self):
        return self.html_soup.find('meta', attrs={'property': "og:title"}).get('content')

    @optional_parsing_function
    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'article-body'}).find_all('a')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'author', parent=True)

        return [a['href'] for a in html_as if a.get('href') is not None]

    @optional_parsing_function
    def _extract_category(self):
        category = self.html_soup.find('div', attrs={'class': 'article-subhead'}).text
        return category

    @optional_parsing_function
    def _extract_explicit_sources(self):
        a_text = self.html_soup.find('span', attrs={'class': 'author'}).a.text
        source = re.search(r', avec (.*)', a_text)
        if source is not None:
            return [source.group(1)]
        return []
