#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'express website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re
from datetime import datetime


class LExpress(GenericMedia):
    """
    Class used for extracting items from french media "L'Express".
    """
    supported_domains = ['www.lexpress.fr', 'lexpansion.lexpress.fr']
    id = 'lexpress'
    display_name = 'L\'Express'

    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'class': 'article_container'})

    def _extract_category(self):
        html_category = self.html_soup.find('div', attrs={'class': 'article_category'}).find('a').text
        return html_category

    def _extract_explicit_sources(self):
        text = self.html_soup.find('span', attrs={'itemprop': 'author'}).span.text
        # Do not want the nominative author
        source = re.search(r'(.*) pour l\'Express', text, re.IGNORECASE)
        if source is None:
            return [text]
        return []
