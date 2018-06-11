#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re


class MediaName(GenericMedia):
    """
    Class used for extracting items from media "".
    """
    supported_domains = ['']
    id = ''
    display_name = ''

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'})

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('ul', attrs={'class': 'breadcrumb'}).find_all('a')[1].text
        return text

    def _extract_explicit_sources(self):
        text = self.html_soup.find('strong', attrs={'rel': 'author'}).text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return [source.group(1)]
        return []
