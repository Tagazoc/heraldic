#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This module backups all URLs in a file.


from heraldic.store.index_searcher import retrieve_all_urls
import sys


def main(argv):
    urllist = retrieve_all_urls()
    with open(argv[0], 'w') as f:
        f.write('\n'.join(urllist))


if __name__ == "__main__":
    main(sys.argv[1:])
