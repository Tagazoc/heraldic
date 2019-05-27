#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.models.document import Document
import heraldic.misc.exceptions as ex
import fileinput
from heraldic.gathering.feeds import UrlFile, UrlList


def gather(args):
    url_list = None
    if args.url:
        url_list = UrlList(args.url, max_depth=args.depth, update_inplace=args.override, raise_on_optional=args.test,
                           dump_result=True)
        url_list.harvest()
    elif args.file:
        url_list = UrlFile(args.file, max_depth=args.depth, update_inplace=args.override, raise_on_optional=args.test,
                           dump_result=True)
        url_list.harvest()
    else:
        for line in fileinput.input():
            url_list = UrlList([line], max_depth=args.depth, update_inplace=args.override, raise_on_optional=args.test, dump_result=True)
            url_list.harvest()

