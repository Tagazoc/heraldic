#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heraldic.store.index_searcher as i_s
from heraldic.gathering.feeds import UrlList


def regather(args):
    errors = i_s.get_similar_errors_urls(args.media, args.attribute, args.error)
    urllist = UrlList(errors, max_depth=args.depth, update_inplace=args.override, raise_on_optional=args.test,
                      crawl_internally=args.crawl_internally, crawl_delay=args.delay, dump_result=args.test)
    urllist.harvest()
