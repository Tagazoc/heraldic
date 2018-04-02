#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module implementing multiple model search.
"""

from src.store import index_searcher
from src.media.known_media import known_media

# TODO récupérer toutes les translations en modèle de index_searcher ici


def search_by_media(media_id: str, limit: int=100):
    if not known_media.media_exists(media_id):
        raise ValueError
    return index_searcher.search(q="media:" + media_id, limit=limit)
