#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.models.document import Document
import heraldic.misc.exceptions as ex
import fileinput
from heraldic.gathering.feeds import UrlFile, UrlList


def gather(args):
    url_list = None
    if args.url:
        url_list = UrlList(args.url)
        url_list.harvest(max_depth=args.depth, update_entries=args.override, raise_on_optional=args.test,
                         dump_result=True)
    elif args.file:
        url_list = UrlFile(args.file)
        url_list.harvest(max_depth=args.depth, update_entries=args.override, raise_on_optional=args.test,
                         dump_result=True)
    else:
        for line in fileinput.input():
            url_list = UrlList([line])
            url_list.harvest(max_depth=args.depth, update_entries=args.override, raise_on_optional=args.test, dump_result=True)

