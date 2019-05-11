#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
from datetime import datetime


class ValeursActuelles(GenericMedia):
    """
    Class used for french media "Valeurs Actuelles".
    """
    supported_domains = ['www.valeursactuelles.com']
    id = 'valeurs_actuelles'
    display_name = 'Valeurs Actuelles'


class ValeursActuellesExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Valeurs Actuelles".
    """
    test_urls = ['https://www.valeursactuelles.com/monde/le-pape-francois-est-il-devenu-le-vicaire-de-la-gauche-immigrationniste-et-de-lislamisme-conquerant-106658']

    def _check_extraction(self):
        return True
        return self.html_soup.select_one('div.articleBody') is not None

    def _extract_body(self):
        content_div = self.html_soup.select_one('article div.field--name-body.field--label-hidden')
        chapo_tag = self.html_soup.select_one('article div.field--name-field-chapo')
        content_div.insert(0, chapo_tag)
        side_links_tags = content_div.select('div.linked-articles')
        self._side_links.extend([tag.extract().a for tag in side_links_tags])
        return content_div

    def _extract_doc_publication_time(self):
        return self.html_soup.find('span', attrs={'property': 'schema:dateCreated'}).get('content')

    def _extract_doc_update_time(self):
        try:
            time_text = self.html_soup.find('meta', attrs={
                'property': "article:modified_time"
            }).get('content')
            return datetime.strptime(time_text[4:], '%d/%m/%Y - %H:%M')
        except AttributeError:
            return None

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        try:
            text = self.html_soup.select_one('div.field--name-field-rubrique').find_all('a')[-1].text
            return text
        except AttributeError:
            return ''

    def _extract_news_agency(self):
        return ''

    def _extract_side_links(self):
        side_links_tags = self.html_soup.select('div.linked-articles')
        self._side_links.extend([tag.extract().a for tag in side_links_tags])
        return self._side_links

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('div.p3-wrapper') is not None
