#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers again all stored documents, for example to use new parsers.

from heraldic.store import index_searcher
from heraldic.models.document import Document
from heraldic.misc.exceptions import DocumentNotChangedException, DomainNotSupportedException


models = index_searcher.search_by_media("le_monde", limit=10000)
for model in models:
    print(model.id.value + " : " + model.urls.value[0])
    d = Document.from_model(model)
    try:
        d.gather(force_update=True)
    except DocumentNotChangedException:
        pass
    except DomainNotSupportedException:
        # DIE !
        d.delete()
