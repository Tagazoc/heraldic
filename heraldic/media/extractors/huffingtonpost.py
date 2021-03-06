#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Huffigton Post website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
from copy import copy
import re


class HuffingtonPost(GenericMedia):
    """
    Class used for media "Huffington Post".
    """
    supported_domains = ['www.huffingtonpost.fr']
    id = 'huffington_post'
    articles_regex = [r'[0-9]{6}/?$']
    display_name = 'Huffington Post'


class HuffingtonPostExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from media "Huffington Post" in french langugage.
    """
    test_urls = ['https://www.huffingtonpost.fr/2019/02/06/la-rencontre-entre-luigi-di-maio-et-des-gilets-'
                 'jaunes-une-nouvelle-provocation-pour-paris_a_23663273/',
                 'https://www.huffingtonpost.fr/2019/03/21/game-of-thrones-saison-8-emilia-clarke-annonce-'
                 'avoir-survecu-a-deux-hemorragies-cerebrales_a_23698096/']
    default_extractor = True

    def _extract_body(self):
        content_div = self.html_soup.select_one('div.post-contents')
        # Body should not be None, but this will be checked in _post_extract_body() (body.text)

        try:
            related_entries_tag = content_div.select_one('div.related-entries').extract()
            self._side_links = related_entries_tag.select('a')
        except AttributeError:
            pass
        try:
            strong = content_div.find_all('strong')
            [s.find(string=re.compile(r'à voir .*', re.IGNORECASE)).parent.parent.decompose() for s in strong]
        except AttributeError:
            pass
        try:
            content_div.blockquote.decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/news/[^/]+/?$')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/tag/[^/]+/?$')
        html_as = self._exclude_hrefs_by_regex(html_as, r'/[^/]+/?$')
        return html_as

    def _extract_category(self):
        span_text = self.html_soup.select_one('span.entry-eyebrow').text
        return span_text

    def _extract_news_agency(self):
        author_tag = self.html_soup.select_one('a.author-card__details__name')
        if author_tag is None:
            author_tag = self.html_soup.select_one('span.author-card__microbio')
        return author_tag


class HuffingtonPostVideoExtractor(HuffingtonPostExtractor):
    """
    Class used for extracting items from pages displaying a video on media "Huffington Post" in french language.
    """
    test_urls = ['https://www.huffingtonpost.fr/2019/02/04/grand-debat-a-evry-cette-maire-a-ose-la-petite-'
                 'blague-face-a-macron_a_23661348/']
    default_extractor = False
    _document_type = 'video'

    def _check_extraction(self):
        return self.html_soup.select_one('div.video-entry__content-info') is not None

    def _extract_body(self):
        return self.html_soup.select_one('div.video-entry__caption')

    def _extract_news_agency(self):
        # No news agency for video
        return None

    def _extract_side_links(self):
        return self.html_soup.select('div.entry-recirc-mod ul a')
