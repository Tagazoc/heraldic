#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers all links in one particular feed.

from src.gathering.feeds import FeedHarvester

OVERRIDE = True
FEED_URL = 'https://mrmondialisation.org/feed/'

harvester = FeedHarvester()
harvester.retrieve_feeds()
harvester.harvest_feed(FEED_URL)
