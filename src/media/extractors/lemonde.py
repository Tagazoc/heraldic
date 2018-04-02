#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.generic_media import GenericMedia, handle_parsing_errors
import re
from datetime import datetime


class LeMonde(GenericMedia):
    """
    Class used for extracting items from french media "Le Monde".
    """
    domains = ['www.lemonde.fr']
    id = 'le_monde'
    display_name = 'Le Monde'

    @handle_parsing_errors
    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'id': 'articleBody'}).text

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
        html_as = self.html_soup.article.find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'lien_interne')
        html_as = self._exclude_hrefs(html_as, 'class', 'lire', parent=True)
        return [a['href'] for a in html_as]

    @handle_parsing_errors
    def _extract_category(self):
        html_nav = self.html_soup.find('nav', attrs={'id': 'nav_ariane'})
        html_title = self.html_soup.find('div', attrs={'class': 'tt_rubrique_ombrelle'}).contents[1].text
        return html_title

    @handle_parsing_errors
    def _extract_explicit_sources(self):
        html_span = self.html_soup.find('span', attrs={'id': 'publisher'})
        data_source = html_span['data-source']
        source = re.search(r' avec (.*)', data_source)
        try:
            sources = source.group(1)
        except AttributeError:
            return []
        sources = sources.split(' et ')
        return sources
