#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module supports all REST actions for docs collection.
"""

import heraldic.misc.exceptions as ex
from heraldic.models.document import Document
from flask import abort


def get_doc(id, with_history):
    d = Document(doc_id=id)
    if d.model.initialized:
        if with_history:
            d.retrieve_old_versions()
        return d.to_json(with_history)
    else:
        abort(
            404, "Document with ID {id} not found".format(id=id)
        )


def get_url(url, with_history):
    d = Document(url)
    if d.model.initialized:
        if with_history:
            d.retrieve_old_versions()
        return d.to_json(with_history)
    else:
        abort(
            404, "Url {url} not found".format(url=url)
        )


def post_url(body):
    url = body['url']
    d = None
    try:
        d = Document(url)
        d.gather()
        return d.model.id.value
    except ex.DomainNotSupportedException as err:
        abort(
            501, "Domain {domain} not implemented".format(domain=err.domain)
        )
    except ex.DocumentExistsException:
        return d.model.id.value
