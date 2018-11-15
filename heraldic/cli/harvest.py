#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.gathering.feeds import FeedHarvester


def harvest(args):
    harvester = FeedHarvester()
    harvester.retrieve_feeds(media_id=args.media)

    harvester.harvest(args.override, max_depth=args.depth)
