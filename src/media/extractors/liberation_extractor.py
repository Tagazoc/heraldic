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
    def _extract_doc_publication_time(self):
        try:
            time_text = self.html_soup.find('span', attrs={'class': 'date'}).time['datetime']
        except AttributeError as err:
            raise HTMLParsingFailureException from err
        return self._format_datetime(time_text[:-3], '%Y-%m-%dT%H:%M')

    @handle_parsing_errors
    def _extract_doc_update_time(self):
        pub_time = self.html_soup.find('span', attrs={'class': 'date'}).time
        update_time = pub_time.next_sibling.next_sibling.text
        try:
            update_datetime = datetime.strptime(update_time[:-3], '%Y-%m-%dT%H:%M')
        except ValueError:
            pub_datetime = datetime.strptime(pub_time['datetime'][:-3], '%Y-%m-%dT%H:%M')
            try:
                update_time = datetime.strptime(update_time, '%H:%M')
            except ValueError:
                return pub_datetime
            update_datetime = datetime.combine(pub_datetime.date(), update_time.time())
        return update_datetime

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
