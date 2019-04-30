#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Parisien's website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
import locale
from datetime import datetime


class LeParisien(GenericMedia):
    """
    Class used for french media "Le Parisien".
    """
    supported_domains = ['www.leparisien.fr', 'videos.leparisien.fr']
    id = 'le_parisien'
    articles_regex = [r'\.php/?$', r'/video/.*-[a-z0-9]+']
    display_name = 'Le Parisien'


class LeParisienExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Parisien".
    """
    test_urls = ['http://www.leparisien.fr/politique/ismael-emelien-proche-conseiller-d-emmanuel-macron'
                 '-demissionne-11-02-2019-8009649.php']
    default_extractor = True

    def _extract_body(self):
        return self.html_soup.select_one('div.article-full__body-content')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select('span.article-full__breadcrumb span')[-1].text
        return text

    def _extract_news_agency(self):
        return self.html_soup.select_one('span.article-full__author-label')


class LeParisienVideoExtractor(GenericMediaExtractor):
    test_urls = ['http://videos.leparisien.fr/video/paris-evacuation-de-la-colline-du-crack-27-06-2018-x6mx5zz']

    default_extractor = False

    def _extract_body(self):
        return self.html_soup.select_one('div.description-full')

    def _check_extraction(self):
        return self.html_soup.select_one('div#contVideoIframe') is not None

    def _extract_doc_publication_time(self):
        date = self.html_soup.select_one('span.date').text
        locale.setlocale(locale.LC_ALL, '')
        return datetime.strptime(date, '%A %d %B %Y ')

