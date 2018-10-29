#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Various functions.


import re
from functools import lru_cache
from heraldic.misc.exceptions import InvalidUrlException


# Regex based on dperini's https://gist.github.com/dperini/729294
url_regex = re.compile(
            # Sometimes there are spaces before the url, browsers accept them
            r'^\s*' +
            # Protocol, sometimes only double slash or nothing
            r'((?:(?:https?:)?//)?)' +
            # domain name construction
            r'(' +
            # host name
            r"(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)" +
            # domain name
            r"(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*" +
            # TLD identifier
            r"(?:\.(?:[a-z\u00a1-\uffff]{2,}))" +
            r')' +
            # TLD may end with dot
            r"\.?" +
            # port number
            r"(?::\d{2,5})?" +
            # resource path
            r"((?:/[^#?]*)?)" +
            # parameters/beacons
            r'(?:\?|#|$)'
        )


@lru_cache(maxsize=1000)
def _match_url(url):
    return url_regex.match(url)


def get_domain(url):
    try:
        match = _match_url(url)
        return match.group(2)
    except AttributeError:
        raise InvalidUrlException(url)


def get_resource(url):
    try:
        match = _match_url(url)
        return match.group(3)
    except AttributeError:
        raise InvalidUrlException(url)


def get_truncated_url(url):
    try:
        match = _match_url(url)

        # Replace protocol scheme if not specified
        protocol_scheme = 'http://' if len(match.group(1)) < 6 else match.group(1)

        return protocol_scheme + match.group(2) + match.group(3)
    except AttributeError:
        raise InvalidUrlException(url)
