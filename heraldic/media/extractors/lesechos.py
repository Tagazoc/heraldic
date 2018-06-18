#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Les Echos website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia
from copy import copy


class LesEchos(GenericMedia):
    """
    Class used for extracting items from french media "Les Echos".
    """
    supported_domains = ['www.lesechos.fr']
    id = 'les_echos'
    display_name = 'Les Echos'

    def _extract_body(self):
        content_div = copy(self.html_soup).find('div', attrs={'class': 'content-article'})
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'block-alireaussi'})]
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'encadre-lireaussi'})]
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'signature-article'})]
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'block-surlemmsujet'})]
        [div.decompose() for div in content_div.find_all('div', attrs={'class': 'encadre'})
         if div.find('div', attrs={'class': 'encadre_titre'}).text.startswith('LIRE AUSSI')]
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('ul', attrs={'class': 'breadcrumbs'}).find_all('span')[-1].text
        return text
