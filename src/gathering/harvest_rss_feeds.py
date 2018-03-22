#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module uses stored feeds to gather and store all documents listed in them.

from src.store import model_searcher


feeds = model_searcher.retrieve_feeds()

for feed in feeds:
    feed.gather()
    if feed.stored_version != feed.current_version:
        feed.harvest()
        feed.update()
