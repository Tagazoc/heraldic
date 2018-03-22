#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module for storing feeds from a CSV file.

from src.gathering.feeds import RssFeed
from src.store import model_searcher
import sys


def main(argv):
    existing_feeds = model_searcher.retrieve_feeds()

    feed_urls = [feed.url for feed in existing_feeds]

    with open(argv[0], 'r') as f:
        for url in f.readlines():
            if url not in feed_urls:
                feed = RssFeed(url)
                feed.store()


if __name__ == "__main__":
    main(sys.argv[1:])
