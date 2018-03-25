#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to know which media are supported and which domain.
"""

from src.media.extractors.liberation_extractor import LiberationExtractor
from src.media.extractors.lemonde_extractor import LeMondeExtractor
from src.media.extractors.lefigaro_extractor import LeFigaroExtractor
from src.heraldic_exceptions import DomainNotSupportedException
from src.misc.logging import logger


class KnownMedia(object):
    def __init__(self):
        self.media_by_domain = {}

        self._set_media_domains()

    def __getitem__(self, domain):
        try:
            return self.media_by_domain[domain]
        except KeyError:
            raise DomainNotSupportedException(domain)

    def _set_media_domains(self):
        for name, val in globals().items():
            try:
                if val.__name__.endswith('Extractor'):
                    for domain in val.domains:
                        self.media_by_domain[domain] = val
            except KeyError:
                continue
            except AttributeError:
                continue

    # def _set_media_domains(self):
    #     for name, val in globals().items():
    #         try:
    #             if val.__name__.endswith('Extractor'):
    #                 self.domains_by_media[val.__name__[:-9]] = val.domains
    #         except AttributeError:
    #             continue


known_media = KnownMedia()
