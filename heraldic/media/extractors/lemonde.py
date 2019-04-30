#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re
from copy import copy


class LeMonde(GenericMedia):
    """
    Class used for french media "Le Monde".
    """
    supported_domains = ['www.lemonde.fr']
    id = 'le_monde'
    articles_regex = [r'\.html$']
    display_name = 'Le Monde'


class LeMondeExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Monde".
    """
    default_extractor = True

    def _check_extraction(self):
        return self.html_soup.article.find('div', attrs={'id': 'articleBody'}) is not None

    def _extract_body(self):
        return self.html_soup.article.find('div', attrs={'id': 'articleBody'})

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        self._exclude_hrefs(html_as, attribute_name='class', attribute_value='lien_interne')
        self._exclude_hrefs(html_as, attribute_name='class', attribute_value='lire', is_parent_attribute=True)

        return html_as

    def _extract_category(self):
        return self.html_soup.select_one('div.tt_rubrique_ombrelle').contents[1].text

    def _extract_news_agency(self):
        data_source = self.html_soup.find('span', attrs={'id': 'publisher'})['data-source']
        source = re.search(r' avec (.*)', data_source)
        try:
            sources = source.group(1)
        except AttributeError:
            return ''
        return sources

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('div.teaser_article') is not None


class LeMondeNewExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Monde" for new article architecture (3rd trimester of 2018).
    """
    test_urls = ['https://www.lemonde.fr/pixels/article/2019/02/10/journalistes-reseaux-sociaux-et-harcelement'
                 '-comprendre-la-polemique-sur-la-ligue-du-lol_5421698_4408996.html',
                 'https://www.lemonde.fr/m-le-mag/article/2019/02/08/d-american-psycho-a-vice-les'
                 '-metamorphoses-de-christian-bale_5420686_4500055.html',
                 'https://www.lemonde.fr/societe/article/2019/02/09/gilets-jaunes-un-manifestant-grievement'
                 '-blesse_5421485_3224.html']

    def _check_extraction(self):
        return self.html_soup.article.select_one('section.article__content') is not None

    def _extract_body(self):
        content_div = self.html_soup.article.select_one('section.article__content')
        side_links = [section.extract().select('a') for section in content_div.select('section.catcher')] \
                     + [section.extract().select('a') for section in content_div.select('div.dfp__inread')]
        try:
            content_div.select_one('section.article__comments').decompose()
        except AttributeError:
            pass
        self._side_links.extend([link for links in side_links for link in links])
        try:
            content_div.select_one('section.author').decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_category(self):
        try:
            return self.html_soup.select_one('li.breadcrumb__parent').a.text
        except AttributeError:
            # On M le Mag, no category sometimes
            return ''

    def _extract_news_agency(self):
        return self.html_soup.find('span', attrs={'class': 'meta__author'})

    def _extract_subscribers_only(self):
        return self.html_soup.select_one('p.article__status') is not None

    def _extract_side_links(self):
        side_links = super(LeMondeNewExtractor, self)._extract_side_links()
        side_links.extend(self.html_soup.select('section.article__siblings-container a'))
        return side_links
