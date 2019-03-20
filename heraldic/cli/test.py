#!/usr/bin/env python
# -*- coding: utf-8 -*-


from heraldic.gathering.feeds import UrlList
from heraldic.media.known_media import known_media
import itertools


def test(args):
    if args.media:
        urls = itertools.chain(*[extractor.test_urls for extractor in known_media[args.media].get_extractors()])
    else:
        urls = itertools.chain(*[extractor.test_urls for media_class in known_media.media_classes for extractor in
                                 media_class.get_extractors()])

    url_list = UrlList(urls)
    url_list.harvest(max_depth=0, update_inplace=True, raise_on_optional=True, dump_result=True)

