#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.gathering.feeds import FeedHarvester, SourceHarvester


def harvest(args):
    if args.sources:
        harvester = SourceHarvester(args.media, update_inplace=args.override, max_depth=args.depth,
                                    crawl_internally=args.crawl_internally, crawl_delay=args.delay,
                                    recursive_step=args.recursive_step)
        harvester.harvest()
    else:
        harvester = FeedHarvester(update_inplace=args.override, max_depth=args.depth,
                                  crawl_internally=args.crawl_internally, crawl_delay=args.delay)
        harvester.retrieve_feeds(media_id=args.media)

        harvester.harvest()
