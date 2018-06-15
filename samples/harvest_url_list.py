#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module gathers all URLs in a file.


from heraldic.gathering.feeds import UrlFile
import sys


def main(argv):
    urllist = UrlFile(argv[0])
    urllist.harvest(max_depth=3)


if __name__ == "__main__":
    main(sys.argv[1:])
