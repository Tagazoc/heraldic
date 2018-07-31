#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers all links in one particular feed.

from heraldic.gathering.feeds import FeedHarvester

OVERRIDE = True
FEED_URL = 'http://www.leparisien.fr/actualites-a-la-une.rss.xml'

harvester = FeedHarvester()
harvester.retrieve_feeds()
harvester.harvest_feed(FEED_URL, OVERRIDE, max_depth=0)
