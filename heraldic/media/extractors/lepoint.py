#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Point website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class LePoint(GenericMedia):
    """
    Class used for media "Le Point".
    """
    supported_domains = ['www.lepoint.fr']
    id = 'le_point'
    articles_regex = [r'\.php/?$']
    display_name = 'Le Point'


class LePointExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Point".
    """

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'art-text'})

    def _extract_title(self):
        return self.html_soup.find('meta', attrs={'property': "og:title"}).get('content')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'^/tags/')
        return html_as

    def _extract_category(self):
        text = self.html_soup.find('nav', attrs={'class': 'breadcrumb'}).find_all('span')[-1].text
        return text

    def _extract_news_agency(self):
        text = self.html_soup.find('span', attrs={'rel': 'author'}).text
        # Do not want the nominative author
        source = re.search(r'par (.*)', text, re.IGNORECASE)
        if source is None:
            return text
        return ''

    def _extract_subscribers_only(self):
        return self.html_soup.find('aside', attrs={'id': 'article-reserve-aux-abonnes'}) is not None
