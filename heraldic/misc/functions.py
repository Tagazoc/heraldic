#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Various functions.


import re
from functools import lru_cache
import heraldic.misc.exceptions as ex
from typing import Tuple
from time import sleep
from heraldic.misc.config import config
from elasticsearch.exceptions import ConnectionTimeout


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

topmost_regex = re.compile(r'(?:.*\.)?([^.]+\.[^.]+)')


@lru_cache(maxsize=1000)
def _match_url(url):
    return url_regex.match(url)


def get_domain(url, only_topmost=False, do_not_log=False):
    try:
        match = _match_url(url)
        if only_topmost:
            return topmost_regex.match(match.group(2)).group(1)
        return match.group(2)
    except AttributeError:
        raise ex.InvalidUrlException(url, do_not_log=do_not_log)


def get_resource(url, do_not_log_on_error=False):
    try:
        match = _match_url(url)
        return match.group(3)
    except AttributeError:
        raise ex.InvalidUrlException(url, do_not_log=do_not_log_on_error)


def get_truncated_url(url, do_not_log_on_error=False) -> Tuple[str, str]:
    try:
        match = _match_url(url)

        # Replace protocol scheme if not specified
        protocol_scheme = 'http://' if len(match.group(1)) < 6 else match.group(1)
        return protocol_scheme, match.group(2) + match.group(3)
    except AttributeError:
        raise ex.InvalidUrlException(url, do_not_log=do_not_log_on_error)


def handle_connection_errors(decorated):
    def wrapper(*args, **kwargs):
        for i in range(0, 1 + int(config['DEFAULT'].get('indexer_retry_count'))):
            try:
                result = decorated(*args, **kwargs)
                return result
            except ConnectionError as err:
                sleep(float(config['DEFAULT'].get('indexer_retry_delay')))
        raise ex.IndexerConnectionError from err
    return wrapper

