#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers all links in one particular feed.

from src.gathering.feeds import FeedHarvester

OVERRIDE = True
FEED_URL = 'https://www.lesechos.fr/rss/rss_une.xml'

harvester = FeedHarvester()
harvester.retrieve_feeds()
harvester.harvest_feed(FEED_URL, OVERRIDE, max_depth=0)
