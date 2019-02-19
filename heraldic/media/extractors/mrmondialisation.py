#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mr Mondialisation website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor


class MrMondialisation(GenericMedia):
    """
    Class used for french media "Mr Mondialisation".
    """
    supported_domains = ['mrmondialisation.org']
    id = 'MrMondialisation'
    articles_regex = [r'mrmondialisation\.org/[^/]+/?']
    display_name = 'Mr Mondialisation'


class MrMondialisationExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Mr Mondialisation".
    """
    test_urls = ['https://mrmondialisation.org/hommage-a-letudiant-decede-lors-dune-livraison-uber-eats/']

    def _extract_body(self):
        body_div = self.html_soup.article.select_one('div.td-post-content')
        try:
            body_div.select('p strong')[-1].decompose()
        except IndexError:
            pass
        return body_div

    def _extract_category(self):
        html_category = self.html_soup.select('a.entry-crumb')[-1].span.text
        return html_category

    def _extract_side_links(self):
        return self.html_soup.select('div.td_block_related_posts a')
