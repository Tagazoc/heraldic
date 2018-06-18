#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Marianne website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
from copy import copy


class Marianne(GenericMedia):
    """
    Class used for extracting items from french media "Marianne".
    """
    supported_domains = ['www.marianne.net']
    id = 'marianne'
    display_name = 'Marianne'

    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'class': 'chapo_body_wrapper'})
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'read-more-wysiwyg'})]

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('div', attrs={'class': 'field-name-field-rubriques'}).find_all('a')[-1].text
        return text

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'class': 'article-subscription'}) is not None
