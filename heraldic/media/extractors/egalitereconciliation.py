#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class EgaliteReconciliation(GenericMedia):
    """
    Class used for media "Egalité & Réconciliation".
    """
    supported_domains = ['www.egaliteetreconciliation.fr']
    id = 'egalite_reconciliation'
    display_name = 'Egalité & réconciliation'


class EgaliteReconciliationExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "Egalité & Réconciliation".
    """
    test_urls = ['https://www.egaliteetreconciliation.fr/Le-judeo-christianisme-arme-de-destruction-massive-du-catholicisme-romain-52567.html',
                 'https://www.egaliteetreconciliation.fr/Isadora-Duncan-devient-une-agence-et-recrute-54771.html']

    def _check_extraction(self):
        return True
        return self.html_soup.select_one('div.entry-content') is not None

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.entry-content')
        try:
            notes_div = self.html_soup.select_one('div.notes')
            content_div.insert(0, notes_div)
        except ValueError:
            pass
        return content_div

    def _extract_title(self):
        return self.html_soup.select_one('h1.entry-title').text.strip()

    def _extract_doc_publication_time(self):
        return self.html_soup.select_one('abbr.published').get('title')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_side_links(self):
        side_links_as = self.html_soup.select('div#renvois_articles h4 a')
        self._side_links.extend(side_links_as)
        side_links_as = self.html_soup.select('div#navigartprecsuiv a')
        self._side_links.extend(side_links_as)
        return self._side_links
