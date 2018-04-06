#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module uses stored feeds to gather and store all documents listed in them.

from src.gathering.feeds import FeedHarvester

OVERRIDE = False
harvester = FeedHarvester()
harvester.retrieve_feeds()
harvester.harvest(OVERRIDE)
