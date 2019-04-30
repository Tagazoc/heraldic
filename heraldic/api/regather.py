#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module supports all REST actions for docs collection.
"""

from heraldic.models.document import Document
from heraldic.store import index_searcher


def get_error_urls(media, attribute, error=''):
    errors_urls = index_searcher.get_similar_errors_urls(media, attribute, error)
    return list(errors_urls)


def post_doc(body):
    doc = Document(body['url'], contents=body['content'], redirection_url=body['redirection_url'])
    doc.gather()
