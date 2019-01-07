#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module supports all REST actions for media collection.
"""

from heraldic.media.known_media import known_media
from flask import abort


def read_all():
    media = known_media.display_names()
    return media


def read_one(id):
    if not known_media.media_exists(id):
        abort(
            404, "Media {media_id} not found".format(media_id=id)
        )

    return known_media[id].get_data()


def counts(id, unit, number):
    if not known_media.media_exists(id):
        abort(
            404, "Media {media_id} not found".format(media_id=id)
        )

    return known_media[id].get_counts(unit, number)
