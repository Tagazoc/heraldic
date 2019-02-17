#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Marianne website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy


class Marianne(GenericMedia):
    """
    Class used for french media "Marianne".
    """
    supported_domains = ['www.marianne.net']
    id = 'marianne'
    display_name = 'Marianne'


class MarianneExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Marianne".
    """
    test_urls = ['https://www.marianne.net/economie/commercants-artisants-petits-patrons-m-le-president'
                 '-entendez-le-premier-employeur-de-france',
                 'https://www.marianne.net/politique/brexit-valerie-pecresse-veut-que-les-britanniques'
                 '-comprennent-leur-douleur',
                 'https://www.marianne.net/politique/europeennes-gilet-jaune-ingrid-levavasseur-abandonne'
                 '-liste-ric']

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.chapo_body_wrapper')
        side_links = [div.extract().select('a') for div in content_div.select('div.read-more-wysiwyg')]
        self._side_links.extend([a for div_a in side_links for a in div_a])
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.select('div.field-name-field-rubriques a')[-1].text
        return text

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('div.article-subscription') is not None

    def _extract_side_links(self):
        self._side_links.extend(self.html_soup.select('ul.list-article-aside a'))
        return self._side_links
