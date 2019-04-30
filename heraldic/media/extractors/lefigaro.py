#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Figaro website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class LeFigaro(GenericMedia):
    """
    Class used for french media "Le Figaro".
    """
    supported_domains = ['www.lefigaro.fr']
    id = 'le_figaro'
    articles_regex = [r'\.php/?$']
    display_name = 'Le Figaro'


class LeFigaroExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Figaro".
    """
    test_urls = ['http://www.lefigaro.fr/sciences/2019/02/07/01008-20190207ARTFIG00201-la-nasa-a-photographie'
                 '-la-sonde-chinoise-sur-la-face-cachee-de-la-lune.php',
                 'http://www.lefigaro.fr/conjoncture/2019/02/07/20002-20190207ARTFIG00194-eoliennes-'
                 'le-tabou-du-recyclage-et-du-cout-du-demantelement.php']

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.fig-content__body')
        lireaussi_tags = content_div.find_all(string=re.compile(r'LIRE AUSSI -'))
        self._side_links.extend([tag.parent.extract().a for tag in lireaussi_tags])

        b_avoiraussi = content_div.find_all(string=re.compile(r'à voir aussi', re.IGNORECASE))
        [self._side_links.extend(p.parent.extract().select('a')) for p in b_avoiraussi]

        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_attribute(html_as, 'class', 'author', parent=True)

        return html_as

    def _extract_category(self):
        span_text = self.html_soup.select_one('li.fig-breadcrumb__item--current span').text
        return span_text

    def _extract_news_agency(self):
        return self.html_soup.select_one('span.fig-content-metas__author')

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('div.fig-premium-paywall') is not None
