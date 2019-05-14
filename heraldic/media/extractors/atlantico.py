#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Atlantico website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class Atlantico(GenericMedia):
    """
    Class used for french media "Atlantico".
    """
    supported_domains = ['www.atlantico.fr']
    id = 'atlantico'
    display_name = 'Atlantico'


class AtlanticoExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Atlantico".
    """
    test_urls = ['https://www.atlantico.fr/pepite/3572278/cedric-villani-critique-le-senateur-pierre-medevielle-qui-assure-que-le-glyphosate-est-moins-cancerogene-que-la-charcuterie-opecst']

    def _check_extraction(self):
        return True
        return self.html_soup.select_one('div.corps-article') is not None

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.corps-article')
        try:
            sources_tag = self.html_soup.select_one('div.source')
            content_div.insert(0, sources_tag)
        except ValueError:
            pass
        return content_div

    def _extract_description(self):
        return self.html_soup.find('meta', attrs={'property': 'og:description'}).get('content')

    def _extract_doc_publication_time(self):
        return self.html_soup.find('span', attrs={'property': 'dc:date dc:created'}).get('content')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select_one('div.header-top div.theme a').text.strip()
        return text

    def _extract_side_links(self):
        side_links_as = self.html_soup.select('div.savoir-plus a')
        self._side_links.extend(side_links_as)
        return self._side_links
