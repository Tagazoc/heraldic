#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"L'Humanité" website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor


class LHumanite(GenericMedia):
    """
    Class used for french media "L'Humanité".
    """
    supported_domains = ['www.humanite.fr']
    id = 'l_humanite'
    articles_regex = [r'/[a-z-0-9]+$']
    display_name = 'L\'Humanité'


class LHumaniteExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "L'Humanité".
    """

    test_urls = ['https://www.humanite.fr/affaire-jeanne-calment-pourquoi-la-these-de-lusurpation'
                 '-didentite-nest-quune-fake-news-667790',
                 'https://www.humanite.fr/sante-publique-la-fausse-bonne-idee-des-soins-de-proximite-667815']

    def _extract_body(self):
        return self.html_soup.select_one('div.field-name-field-news-text')

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')

        return html_as

    def _extract_category(self):
        text = self.html_soup.find('div', attrs={'id': 'block-system-main-menu'}).\
            select_one('ul.menu a.active').text
        return text

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'id': 'non-abonnes-link-url'}) is not None

    def _extract_side_links(self):
        return self.html_soup.select('div.field-name-block-similar-contents a')
