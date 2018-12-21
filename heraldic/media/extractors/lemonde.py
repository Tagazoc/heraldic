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
        content_div = copy(self.html_soup.article.find('div', attrs={'id': 'articleBody'}))
        return content_div

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        self._exclude_hrefs(html_as, attribute_name='class', attribute_value='lien_interne')
        self._exclude_hrefs(html_as, attribute_name='class', attribute_value='lire', is_parent_attribute=True)

        return html_as

    def _extract_category(self):
        return self.html_soup.find('div', attrs={'class': 'tt_rubrique_ombrelle'}).contents[1].text

    def _extract_news_agency(self):
        data_source = self.html_soup.find('span', attrs={'id': 'publisher'})['data-source']
        source = re.search(r' avec (.*)', data_source)
        try:
            sources = source.group(1)
        except AttributeError:
            return ''
        return sources

    def _extract_subscribers_only(self):
        return self.html_soup.find('div', attrs={'class': 'teaser_article'}) is not None


class LeMondeNewExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Monde" for new article architecture (3rd trimeester of 2018).
    """
    def _check_extraction(self):
        return self.html_soup.article.find('section', attrs={'class': 'article__content'}) is not None

    def _extract_body(self):
        content_div = copy(self.html_soup.article.find('section', attrs={'class': 'article__content'}))
        [section.decompose() for section in content_div.find_all('section', attrs={'class': 'catcher'})]
        [section.decompose() for section in content_div.find_all('div', attrs={'class': 'dfp__inread'})]
        return content_div

    def _extract_category(self):
        return self.html_soup.find('li', attrs={'class': 'breadcrumb__parent'}).a.text

    def _extract_news_agency(self):
        data_source = self.html_soup.find('span', attrs={'class': 'meta__author'}).text

        source = re.search(r' avec (.*)', data_source)
        try:
            sources = source.group(1)
        except AttributeError:
            return ''
        return sources

    def _extract_subscribers_only(self):
        return self.html_soup.find('p', attrs={'class': 'article__status'}) is not None
