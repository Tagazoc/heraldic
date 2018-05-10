#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Point website extractor implementation.
"""

from src.media.generic_media import GenericMedia, optional_parsing_function, mandatory_parsing_function
import re


class LePoint(GenericMedia):
    """
    Class used for extracting items from media "".
    """
    domains = ['www.lepoint.fr']
    id = 'le_point'
    display_name = 'Le Point'

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

    def _extract_explicit_sources(self):
        text = self.html_soup.find('span', attrs={'rel': 'author'}).text
        # Do not want the nominative author
        source = re.search(r'par (.*)', text, re.IGNORECASE)
        if source is None:
            return [text]
        return []

    def _extract_subscribers_only(self):
        return self.html_soup.find('aside', attrs={'id': 'article-reserve-aux-abonnes'}) is not None
