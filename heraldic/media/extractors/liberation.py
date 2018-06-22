#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re


class Liberation(GenericMedia):
    """
    Class used for extracting items from french media "Libération".
    """
    supported_domains = ['www.liberation.fr']
    id = 'liberation'
    display_name = 'Libération'

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'class': 'article-body'})

    def _extract_title(self):
        return self.html_soup.find('meta', attrs={'property': "og:title"}).get('content')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'author', parent=True)

        return html_as

    def _extract_category(self):
        category = self.html_soup.find('div', attrs={'class': 'article-subhead'}).text
        return category

    def _extract_news_agency(self):
        a_text = self.html_soup.find('span', attrs={'class': 'author'}).a.text
        source = re.search(r', avec (.*)', a_text)
        if source is not None:
            return source.group(1)
        return ''
