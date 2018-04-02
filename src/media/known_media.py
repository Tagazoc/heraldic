#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to know which media are supported and which domain.
"""

from typing import Set
from src.media import extractors
from src.media.extractors.media_extractor import MediaExtractor
from src.heraldic_exceptions import DomainNotSupportedException
from src.misc.logging import logger
import pkgutil
import inspect
from src.store import index_searcher


class KnownMedia(object):
    def __init__(self):

        self.media_classes: Set[MediaExtractor] = set()

        self._set_media_classes()

    def __getitem__(self, media_name):
        for media in self.media_classes:
            if media.media_name == media_name:
                return media

    def get_media_by_domain(self, domain) -> MediaExtractor:
        for media_class in self.media_classes:
            if domain in media_class.domains:
                return media_class
        raise DomainNotSupportedException(domain)

    def media_exists(self, media_name: str) -> bool:
        return media_name in self.names

    def display_names(self):
        return {media.media_name: media.display_name for media in self.media_classes}

    @property
    def names(self):
        return [media.media_name for media in self.media_classes]

    def _set_media_classes(self):
        # Get all modules from extractors
        for importer, modname, ispkg in pkgutil.iter_modules(extractors.__path__):
            module = importer.find_module(modname).load_module(modname)
            # Get classes defined in module, and add them to media_classes attribute
            classes = inspect.getmembers(module, inspect.isclass)
            extractor_classes = [class_[1] for class_ in classes if class_[1].__module__.endswith(modname)]
            self.media_classes = self.media_classes.union(extractor_classes)


known_media = KnownMedia()
