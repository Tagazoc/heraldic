#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module uses stored feeds to gather and store all documents listed in them.

from heraldic.gathering.feeds import FeedHarvester

OVERRIDE = False
MAX_DEPTH = 0
harvester = FeedHarvester()
harvester.retrieve_feeds()
harvester.harvest(OVERRIDE, max_depth=MAX_DEPTH)
