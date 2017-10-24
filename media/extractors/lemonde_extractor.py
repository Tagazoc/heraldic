#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.generic_media_extractor import GenericMediaExtractor
import re
from datetime import datetime


class LeMondeExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Monde".
    """
    domains = ['www.lemonde.fr']
    media_name = 'le_monde'

    def _extract_document_body(self):
        return self.html_soup.article.find('div', attrs={'id': 'articleBody'}).text

    def _extract_publication_timestamp(self):
        time_text = self.html_soup.find('time', attrs={'itemprop': 'datePublished'}).text
        return datetime.strptime(time_text, '%d.%m.%Y &agrave; %Hh%M')

    def _extract_update_timestamp(self):
        time_text = self.html_soup.find('time', attrs={'itemprop': 'dateModified'}).text
        return datetime.strptime(time_text, '%d.%m.%Y &agrave; %Hh%M')

    def _extract_href_sources(self):
        html_as = self.html_soup.article.find_all('a')
        html_as = self._exclude_hrefs(html_as, 'class', 'lien_interne')
        html_as = self._exclude_hrefs(html_as, 'class', 'lire', parent=True)
        return [a['href'] for a in html_as]

    def _extract_category(self):
        html_nav = self.html_soup.find('nav', attrs={'id': 'nav_ariane'})
        return html_nav['class'][0]

    def _extract_explicit_sources(self):
        html_span = self.html_soup.find('span', attrs={'id': 'publisher'})
        data_source = html_span['data-source']
        source = re.search(r' avec (.*)', data_source)
        return [source.group(1)]
