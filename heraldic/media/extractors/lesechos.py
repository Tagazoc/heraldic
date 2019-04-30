#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Les Echos website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy


class LesEchos(GenericMedia):
    """
    Class used for french media "Les Echos".
    """
    supported_domains = ['www.lesechos.fr']
    id = 'les_echos'
    articles_regex = [r'(?:-\d+)(\.php)?/?$']
    display_name = 'Les Echos'


class LesEchosExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Les Echos".
    """
    test_urls = ['https://www.lesechos.fr/monde/europe/0600678884182-brexit-may-tentee-par-la-strategie-de-'
                 'la-derniere-ligne-droite-2243862.php']

    def _extract_body(self):
        soup_copy = copy(self.html_soup)
        content_div = soup_copy.select('article>div>div>div>div>div>div>div>div')[1]

        side_links_divs = [div.extract() for div in content_div.select('div.block-alireaussi')]\
                          + [div.extract() for div in content_div.select('div.encadre-lire-aussi')]\
                          + [div.extract() for div in content_div.select('div.signature-article')]\
                          + [div.extract() for div in content_div.select('div.block-surlemmsujet')]
        self._side_links.extend([a for div in side_links_divs for a in div.select('a')])
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        # Vernimmen definitions are not real articles
        # Well, they are, but not news, you understood me Mr. Seux.
        # I miss B. Maris, too.
        html_as = self._exclude_hrefs_by_regex(html_as, r'/finance-marches/vernimmen/')

        return html_as

    def _extract_category(self):
        return self.html_soup.select_one('article>div>header>ul>li>a>span').text
