#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Various functions.


import re


def get_domain(url):
    domain_regex = re.compile(r'https?://(.*?)/')
    try:
        match = domain_regex.match(url)
        return match.group(1)
    except AttributeError:
        raise ValueError
