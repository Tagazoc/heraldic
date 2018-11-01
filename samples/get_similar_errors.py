#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers all links in one particular feed.

import heraldic.store.index_searcher as i_s
from heraldic.gathering.feeds import UrlList
import sys


def main(argv):
    errors = i_s.get_similar_errors_urls(argv[0], argv[1])
    print(len(errors))
    urllist = UrlList()
    urllist.entries = errors
    urllist.harvest()


if __name__ == "__main__":
    main(sys.argv[1:])


