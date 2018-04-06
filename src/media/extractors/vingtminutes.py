#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
20 minutes website extractor implementation.
"""

from src.media.generic_media import GenericMedia, handle_parsing_errors
import re
from datetime import datetime


class VingtMinutes(GenericMedia):
    """
    Class used for extracting items from french media "20 Minutes".
    """
    domains = ['www.20minutes.fr']
    id = '20minutes'
    display_name = '20 Minutes'

    @handle_parsing_errors
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'content'}).text

    @handle_parsing_errors
    def _extract_doc_publication_time(self):
        time_text = self.html_soup.find('time').get('datetime')
        return datetime.strptime(time_text[:-6], '%Y-%m-%dT%H:%M:%S')

    @handle_parsing_errors
    def _extract_doc_update_time(self):
        try:
            time_text = self.html_soup.find_all('time')[1].get('datetime')
            return datetime.strptime(time_text[:-6], '%Y-%m-%dT%H:%M:%S')
        except AttributeError:
            return None

    @handle_parsing_errors
    def _extract_href_sources(self):
        html_as = self.html_soup.article.find('div', attrs={'class': 'content'}).find_all('a')

        # Exclude tags & share buttons links
        tags_as = self.html_soup.article.find('div', attrs={'class': 'tags'}).find_all('a')
        sharebar_as = self.html_soup.article.find('div', attrs={'class': 'sharebar'}).find_all('a')
        html_as = [a for a in html_as if a not in tags_as and a not in sharebar_as]

        # Also exclude internal links for groups of articles
        html_as = self._exclude_hrefs_by_regex(html_as, r'/dossier/')

        # And "generic" links, which seem to end with "/" :
        html_as = self._exclude_hrefs_by_regex(html_as, r'/$')

        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_category(self):
        html_category = self.html_soup.find('span', attrs={'class': 'teaser-headline'}).text
        return html_category
