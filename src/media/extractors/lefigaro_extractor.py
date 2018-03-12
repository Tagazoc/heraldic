#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.document_extractor import DocumentExtractor, handle_parsing_errors
import re
from datetime import datetime
from src.heraldic_exceptions import HTMLParsingFailureException, DateFormatFailureException


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
        html_as = self.html_soup.find('article').find_all('a')

        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_doc_publication_time(self):
        time_text = self.html_soup.find('li', attrs={'class': 'fig-content-metas__pub-date'}).time.text
        try:
            pub_time = datetime.strptime(time_text, 'le %d/%m/%Y à %H:%M')
        except ValueError as err:
            raise DateFormatFailureException(err.args[0])
        return pub_time

    @handle_parsing_errors
    def _extract_doc_update_time(self):
        time_text = self.html_soup.find('li', attrs={'class': 'fig-content-metas__maj-date'}).time.text
        return datetime.strptime(time_text, 'le %d/%m/%Y à %H:%M')

    @handle_parsing_errors
    def _extract_category(self):
        html_li = self.html_soup.find('li', attrs={'class': 'fig-breadcrumb__item--current'})
        span_text = html_li.find('span').text
        return span_text

    @handle_parsing_errors
    def _extract_explicit_sources(self):
        span_text = self.html_soup.find('span', attrs={'class': 'fig-content-metas__author'}).text
        source = re.search(r' avec (\S*)', span_text)
        return [source.group(1)]
