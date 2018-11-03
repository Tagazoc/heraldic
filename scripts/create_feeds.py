#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module for storing feeds from a CSV file.

from heraldic.gathering.feeds import FeedHarvester, RssFeed
import sys
from heraldic.store.elastic import FeedsIndex


def main(argv):
    harvester = FeedHarvester()
    harvester.retrieve_feeds()

    feed_urls = [feed.url for feed in harvester.feeds]
    FeedsIndex.delete()
    FeedsIndex.create()

    with open(argv[0], 'r') as f:
        for url in f.readlines():
            if url not in feed_urls:
                feed = RssFeed(url)
                feed.gather()
                feed.store()


if __name__ == "__main__":
    main(sys.argv[1:])