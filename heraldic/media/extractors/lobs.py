#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'Obs website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
import json
from copy import copy


class LObs(GenericMedia):
    """
    Class used for french media "L'Obs".
    """
    supported_domains = ['www.nouvelobs.com', 'bibliobs.nouvelobs.com']
    id = 'l_obs'
    articles_regex = [r'\.html$']
    display_name = 'L\'Obs'


class LObsExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "L'Obs".
    """
    test_urls = ['https://www.nouvelobs.com/monde/l-amerique-selon-trump/20190214.OBS0230/donald-trump-va-'
                 'declarer-l-urgence-nationale-pour-financer-le-mur-a-la-frontiere-mexicaine.html',
                 'https://bibliobs.nouvelobs.com/documents/20190214.OBS0216/salman-rushdie-je-suis-devenu'
                 '-le-personnage-d-un-mauvais-roman-d-espionnage.html']

    def _extract_body(self):
        content_div = self.html_soup.find('div', attrs={'id': 'ObsArticle-body'})
        self._side_links = content_div.select('a.lire')
        # Make a copy of content div to avoid changing whole htmlsoup
        content_div = copy(content_div)
        [readmore_a.decompose() for readmore_a in content_div.select('a.lire')]
        content_div.select_one('p.author').decompose()
        try:
            content_div.select_one('div.ObsPaywall').decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_doc_publication_time(self):
        data = json.loads(self.html_soup.find('script', type='application/ld+json').text)
        return data['datePublished']

    def _extract_doc_update_time(self):
        data = json.loads(self.html_soup.find('script', type='application/ld+json').text)
        return data['dateModified']

    def _extract_href_sources(self):
        html_as = self._body_tag.select('a')
        html_as = self._exclude_hrefs_by_regex(html_as, r'.*/$')
        return html_as

    def _extract_category(self):
        text = self.html_soup.select('nav.breadcrumb a')[-1].text
        return text

    def _extract_news_agency(self):
        author = self.html_soup.select_one('div.ObsArticle-author span').text
        source = re.search(r' avec (.*)', author)
        if source is not None:
            return source.group(1)
        try:
            text = self._body_tag.select('strong')[-1].text
            source = re.search(r'Avec (.*)\)', text)
            if source is not None:
                return source.group(1)
        except IndexError:
            pass
        return ''

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('div.ObsPaywall') is not None

    def _extract_side_links(self):
        return self.html_soup.select('aside.ObsArticle-related a')

