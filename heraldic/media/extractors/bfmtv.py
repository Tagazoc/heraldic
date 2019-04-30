#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BFM TV website extractor implementation.
"""

from heraldic.media.generic_media import GenericMedia, GenericMediaExtractor
import re


class BfmTv(GenericMedia):
    """
    Class used for french media "BFM TV".
    """
    supported_domains = ['www.bfmtv.com']
    id = 'bfm_tv'
    articles_regex = [r'\.html$']
    display_name = 'BFM TV'


class BfmTvExtractor(GenericMediaExtractor):
    """
    Class used for extracting items from french media "BFM TV".
    """
    test_urls = ['https://www.bfmtv.com/politique/hulot-de-retour-en-forme-sur-la-scene-mediatique-apres-'
                 '3-mois-de-silence-1571892.html']
    default_extractor = True

    def _extract_body(self):
        return self.html_soup.find('div', attrs={'itemprop': 'articleBody'})

    def _extract_category(self):
        text = self.html_soup.select('ul.breadcrumb a')[1].text
        return text

    def _extract_news_agency(self):
        return self.html_soup.find('strong', attrs={'rel': 'author'})

    def _extract_side_links(self):
        return self.html_soup.select('ul.related-article a')


class BfmTvVideoExtractor(GenericMediaExtractor):
    test_urls = ['https://www.bfmtv.com/mediaplayer/video/pour-razzy-hamadi-richard-ferrand-persiste-dans-'
                 'l-erreur-en-refusant-de-demissionner-950369.html']
    _document_type = 'video'
    default_extractor = False

    def _extract_body(self):
        content_div = self.html_soup.find('h2', attrs={'itemprop': 'description'})
        try:
            content_div.find(string="BFMTV, 1ère chaine d'information en continu de France").parent.decompose()
        except AttributeError:
            pass
        return content_div

    def _extract_doc_publication_time(self):
        return self.html_soup.find('meta', attrs={
            'property': "og:video:release_date"
        }).get('content')

    def _check_extraction(self):
        return self.html_soup.select_one('#page-video') is not None
