#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
L'express website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class LExpress(GenericMedia):
    """
    Class used for french media "L'Express".
    """
    supported_domains = ['www.lexpress.fr', 'lexpansion.lexpress.fr']
    id = 'lexpress'
    articles_regex = [r'\.html$']
    display_name = 'L\'Express'


class LExpressExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "L'Express".
    """
    test_urls = ['https://www.lexpress.fr/actualite/politique/contrats-russes-mediapart-leve-le-voile-'
                 'sur-les-millions-de-benalla_2061798.html',
                 'https://www.lexpress.fr/actualite/societe/pour-52-des-francais-les-gilets-jaunes-doivent-'
                 's-arreter_2062700.html']

    def _extract_body(self):
        content_div = self.html_soup.article.select_one('div.article_container')
        side_links_tags = [strong.parent for strong in content_div.select('p strong')
                           if strong.text.startswith('LIRE AUSSI')]

        side_links_tags.extend(content_div.select('div.block_summary_gpt'))

        self._side_links.extend([a for tag in side_links_tags for a in tag.extract().select('a')])
        return content_div

    def _extract_category(self):
        try:
            html_category = self.html_soup.select_one('div.article_category a').text
        except AttributeError:
            html_category = self.html_soup.select('nav.breadcrumb ul.list_inbl li')[-1].find('span').text
        return html_category

    def _extract_href_sources(self):
        html_as = self._body_tag.find_all('a')
        html_as = self._exclude_hrefs_by_parent_tag(html_as, ['em', 'strong'])
        return html_as

    def _extract_news_agency(self):
        text = self.html_soup.find('span', attrs={'itemprop': 'author'}).span.text
        # Do not want the nominative author
        source = re.match(r'(.*) pour l\'Express', text, re.IGNORECASE) or re.match(r'Par (.*)', text, re.IGNORECASE)\
                 or re.match(r'LEXPRESS\.fr avec (.*)', text, re.IGNORECASE)
        if source is not None:
            return source.group(1)
        return ''
