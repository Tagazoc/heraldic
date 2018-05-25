#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to know which media are supported and which domain.
"""

from typing import Set
from src.media import extractors
from src.media.generic_media import GenericMedia
from src.misc.exceptions import DomainNotSupportedException
import pkgutil
import inspect


class KnownMedia(object):
    def __init__(self):

        self.media_classes: Set[GenericMedia] = set()

        self._set_media_classes()

    def __getitem__(self, media_name):
        for media in self.media_classes:
            if media.id == media_name:
                return media

    def get_media_by_domain(self, domain, is_subdomain=False, log_failure=True) -> GenericMedia:
        for media_class in self.media_classes:
            if domain in media_class.supported_domains:
                return media_class
            if is_subdomain:
                for topmost_domain in media_class.topmost_domains():
                    if domain.endswith(topmost_domain):
                        return media_class
        raise DomainNotSupportedException(domain, log=log_failure)

    def media_exists(self, media_id: str) -> bool:
        return media_id in self.names

    def display_names(self):
        return {media.id: media.display_name for media in self.media_classes}

    @property
    def names(self):
        return [media.id for media in self.media_classes]

    def _set_media_classes(self):
        # Get all modules from extractors
        for importer, modname, ispkg in pkgutil.iter_modules(extractors.__path__):
            module = importer.find_module(modname).load_module(modname)
            # Get classes defined in module, and add them to media_classes attribute
            classes = inspect.getmembers(module, inspect.isclass)
            extractor_classes = [class_[1] for class_ in classes if class_[1].__module__.endswith(modname)]
            self.media_classes = self.media_classes.union(extractor_classes)


known_media = KnownMedia()
