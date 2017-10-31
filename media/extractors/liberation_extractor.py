#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.generic_media_extractor import GenericMediaExtractor
import re
from datetime import datetime, time


class LiberationExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Libération".
    """
    domains = ['www.liberation.fr']
    media_name = 'liberation'

    def _extract_document_body(self):
        return self.html_soup.find('div', attrs={'class': 'article-body'}).text

    def _extract_publication_timestamp(self):
        time_text = self.html_soup.find('span', attrs={'class': 'date'}).time['datetime']
        return datetime.strptime(time_text[:-3], '%Y-%m-%dT%H:%M')

    def _extract_update_timestamp(self):
        pub_time = self.html_soup.find('span', attrs={'class': 'date'}).time
        pub_datetime = datetime.strptime(pub_time['datetime'][:-3], '%Y-%m-%dT%H:%M')
        update_time = pub_time.next_sibling.next_sibling.text
        try:
            update_datetime = datetime.strptime(update_time[:-3], '%Y-%m-%dT%H:%M')
        except ValueError:
            update_time = datetime.strptime(update_time, '%H:%M')
            update_datetime = datetime.combine(pub_datetime.date(), update_time.time())
        return update_datetime

    def _extract_href_sources(self):
        html_as = self.html_soup.find('div', attrs={'class': 'article-body'}).find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'author', parent=True)

        return [a['href'] for a in html_as]

    def _extract_category(self):
        category = self.html_soup.find('div', attrs={'class': 'article-subhead'}).text
        return category

    def _extract_explicit_sources(self):
        a_text = self.html_soup.find('span', attrs={'class': 'author'}).a.text
        source = re.search(r', avec (.*)', a_text)
        return [source.group(1)]
