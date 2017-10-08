#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Le Monde website extractor implementation.
"""

from src.media.extractors.generic_media_extractor import GenericMediaExtractor
import re


class LeFigaroExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "Le Figaro".
    """
    domains = ['www.lefigaro.fr']
    media_name = 'le_figaro'

    def _extract_document_body(self):
        return self.html_soup.find('div', attrs={'class': 'fig-content__body'}).text

    def _extract_quotes(self):
        quotes = []
        article_body = self.html_soup.find('div', attrs={'class': 'fig-content__body'}).text
        quote_re = r'"(.*?)"'
        while True:
            try:
                match = re.search(quote_re, article_body)
                quote = match.group(1)
                quotes.append(quote)
                article_body = re.sub(quote_re, "_", article_body, 1)
            except AttributeError:
                break
        return quotes

    def _extract_href_sources(self):
        html_as = self.html_soup.find('article').find_all('a')

        return [a['href'] for a in html_as]

    def _extract_category(self):
        html_li = self.html_soup.find('li', attrs={'class': 'fig-breadcrumb__item--current'})
        span_text = html_li.find('span', attrs={'itemprop': 'name'}).text
        return span_text

    def _extract_explicit_sources(self):
        span_text = self.html_soup.find('span', attrs={'class': 'fig-content-metas__author'}).text
        source = re.search(r' avec (\S*)', span_text)
        return [source.group(1)]
