#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers again all stored documents, for example to use new parsers.

from src.models import model_searcher
from src.models.document import Document
from src.misc.exceptions import DocumentNotChangedException, DomainNotSupportedException


models = model_searcher.search_by_media("le_monde")
for model in models:
    print(model.id.value + " : " + model.urls.value[0])
    d = Document.from_model(model)
    try:
        d.gather(override=True)
    except DocumentNotChangedException:
        pass
    except DomainNotSupportedException:
        # DIE !
        d.delete()
