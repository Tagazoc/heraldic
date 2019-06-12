#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.gathering.feeds import ErrorHarvester, SourceHarvester


def regather(args):
    if args.attribute:
        urllist = ErrorHarvester(args.media, error_attribute=args.attribute, error_body=args.error, max_depth=args.depth,
                                 update_inplace=args.override, raise_on_optional=args.test,
                                 crawl_internally=args.crawl_internally, crawl_delay=args.delay, dump_result=args.test)
    else:
        urllist = SourceHarvester(args.media,
                                  max_depth=args.depth,
                                  update_inplace=args.override, raise_on_optional=args.test, sources_only=False,
                                  crawl_internally=args.crawl_internally, crawl_delay=args.delay, dump_result=args.test)
    urllist.harvest()
