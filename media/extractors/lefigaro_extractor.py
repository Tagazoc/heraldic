#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.generic_media_extractor import GenericMediaExtractor
import re
from datetime import datetime


class LeFigaroExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Figaro".
    """
    domains = ['www.lefigaro.fr']
    media_name = 'le_figaro'

    def _extract_document_body(self):
        return self.html_soup.find('div', attrs={'class': 'fig-content__body'}).text

    def _extract_href_sources(self):
        html_as = self.html_soup.find('article').find_all('a')

        return [a['href'] for a in html_as]

    def _extract_publication_timestamp(self):
        time_text = self.html_soup.find('li', attrs={'class': 'fig-content-metas__pub-date'}).time.text
        return datetime.strptime(time_text, 'le %d/%m/%Y à %H:%M')

    def _extract_update_timestamp(self):
        time_text = self.html_soup.find('time', attrs={'class': 'fig-content-metas__maj-date'}).time.text
        return datetime.strptime(time_text, 'le %d/%m/%Y à %H:%M')

    def _extract_category(self):
        html_li = self.html_soup.find('li', attrs={'class': 'fig-breadcrumb__item--current'})
        span_text = html_li.find('span', attrs={'itemprop': 'name'}).text
        return span_text

    def _extract_explicit_sources(self):
        span_text = self.html_soup.find('span', attrs={'class': 'fig-content-metas__author'}).text
        source = re.search(r' avec (\S*)', span_text)
        return [source.group(1)]
