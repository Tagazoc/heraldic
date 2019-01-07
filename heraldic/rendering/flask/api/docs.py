#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module supports all REST actions for docs collection.
"""

import heraldic.store.index_searcher as i_s
import heraldic.misc.exceptions as ex
from flask import abort


def get_url(url):
    try:
        model = i_s.retrieve_model_from_url(url)
        return {k: v.value for k, v in model.attributes.items() if v.displayable}
    except ex.DocumentNotFoundException:
        abort(
            404, "Url {url} not found".format(url=url)
        )


