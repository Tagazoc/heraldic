#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create all indices.
"""


from heraldic.store.elastic import DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex

DocumentIndex.create()
OldVersionIndex.create()
ErrorIndex.create()
SuggestionIndex.create()
FeedsIndex.create()
