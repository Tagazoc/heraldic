#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'express website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
import re


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

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_parent_tag(html_as, ['em', 'strong'])
        return html_as

    def _extract_news_agency(self):
        text = self.html_soup.find('span', attrs={'itemprop': 'author'}).span.text
        # Do not want the nominative author
        source = re.match(r'(.*) pour l\'Express', text, re.IGNORECASE) or re.match(r'Par (.*)', text, re.IGNORECASE)
        if source is None:
            return text
        return ''
