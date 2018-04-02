#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.document_extractor import DocumentExtractor, handle_parsing_errors
import re
from datetime import datetime, time
from src.heraldic_exceptions import HTMLParsingFailureException, DateFormatFailureException


class LiberationExtractor(DocumentExtractor):
    """
    Class used for extracting items from french media "Libération".
    """
    domains = ['www.liberation.fr']
    media_name = 'liberation'

    @handle_parsing_errors
    def _extract_body(self):
        try:
            body = self.html_soup.find('div', attrs={'class': 'article-body'}).text
        except AttributeError as err:
            raise HTMLParsingFailureException from err
        return body

    @handle_parsing_errors
    def _extract_title(self):
        return self.html_soup.find('meta', attrs={'property': "og:title"}).get('content')

    @handle_parsing_errors
    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'article-body'}).find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'author', parent=True)

        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_category(self):
        category = self.html_soup.find('div', attrs={'class': 'article-subhead'}).text
        return category

    @handle_parsing_errors
    def _extract_explicit_sources(self):
        a_text = self.html_soup.find('span', attrs={'class': 'author'}).a.text
        source = re.search(r', avec (.*)', a_text)
        return [source.group(1)]
