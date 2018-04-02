#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.document_extractor import DocumentExtractor, handle_parsing_errors
import re
from datetime import datetime
from src.heraldic_exceptions import DateFormatFailureException


class LeFigaroExtractor(DocumentExtractor):
    """
    Class used for extracting items from french media "Le Figaro".
    """
    domains = ['www.lefigaro.fr']
    media_name = 'le_figaro'

    @handle_parsing_errors
    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'fig-content__body'}).text

    @handle_parsing_errors
    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'fig-content__body'}).find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'author', parent=True)

        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_category(self):
        html_li = self.html_soup.find('li', attrs={'class': 'fig-breadcrumb__item--current'})
        span_text = html_li.find('span').text
        return span_text
