#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'Obs website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
import json
from copy import copy


class LObs(GenericMedia):
    """
    Class used for french media "L'Obs".
    """
    supported_domains = ['www.nouvelobs.com']
    id = 'l_obs'
    display_name = 'L\'Obs'


class LObsExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "L'Obs".
    """
    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'id': 'ObsArticle-body'})
        [readmore_a.decompose() for readmore_a in content_div.find_all('a', attrs={'class': 'lire'})]
        content_div.find('p', attrs={'class': 'author'}).decompose()
        try:
            content_div.find('div', attrs={'class': 'ObsPaywall'}).decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_doc_publication_time(self):
        data = json.loads(self.html_soup.find('script', type='application/ld+json').text)
        return data['datePublished']

    def _extract_doc_update_time(self):
        data = json.loads(self.html_soup.find('script', type='application/ld+json').text)
        return data['dateModified']

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'.*/$')
        return html_as

    def _extract_category(self):
        text = self.html_soup.find('nav', attrs={'class': 'breadcrumb'}).find_all('a')[-1].text
        return text

    def _extract_news_agency(self):
        text = self.html_soup.find_all('strong')[-1].text
        source = re.search(r' avec (.*)', text)
        if source is not None:
            return source.group(1)
        return ''

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'class': 'ObsPaywall'}) is not None
