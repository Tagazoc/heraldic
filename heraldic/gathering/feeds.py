#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from heraldic.models.document import Document
import heraldic.misc.exceptions as ex
from heraldic.store import index_storer, index_searcher
from typing import List
from datetime import datetime, timedelta
from time import mktime
from heraldic.misc.logging import logger
from heraldic.misc.functions import get_truncated_url
from requests.exceptions import RequestException


class UrlList:
    def __init__(self):
        
        self.gathered_urls = set()
        self.entries = []

        self._counts = {
            'gathered': 0,
            'exist': 0,
            'not_supported': 0,
            'errors': 0
        }

        self._inside_counts = {
            'gathered': 0,
            'total': 0,
            'exist': 0,
            'not_supported': 0,
            'errors': 0
        }

    def harvest(self, update_entries=True, max_depth=0):
        self._gather_links(self.entries, update_entries=update_entries, max_depth=max_depth)

    def _gather_links(self, items: List, update_entries=False, max_depth=0, depth=0):
        counts = self._counts if depth == 0 else self._inside_counts
        for item in items:

            try:
                # items are feed entries
                url = item['link']
                update_time = datetime.fromtimestamp(mktime(item['updated_parsed']))
            except KeyError:
                url = item['link']
                update_time = datetime.fromtimestamp(mktime(item['published_parsed']))
            except TypeError:
                # items are only links
                url = item
                update_time = None

            d = None
            try:
                url = get_truncated_url(url)
                if url in self.gathered_urls:
                    continue
                self.gathered_urls = self.gathered_urls.union([url])
                d = Document(url)
                d.gather(update_time=update_time, update=update_entries)
                self.gathered_urls = self.gathered_urls.union(d.model.urls.value)
                counts['gathered'] += 1
            except ex.DocumentExistsException:
                counts['exist'] += 1
                continue
            except ex.DomainNotSupportedException:
                counts['not_supported'] += 1
                continue
            except ex.GatherError:
                counts['errors'] += 1
                continue
            except ConnectionError:
                counts['errors'] += 1
                continue
            except RequestException:
                counts['errors'] += 1
                continue

            if max_depth > depth:
                inside_links = d.model.href_sources.value
                self._inside_counts['total'] += len(inside_links)
                # Gather internal links, but without updating existing documents
                self._gather_links(inside_links, update_entries=False, max_depth=max_depth, depth=depth + 1)


class RssFeed(UrlList):
    def __init__(self, feed_url, update_time=None, feed_id=None):
        super(RssFeed, self).__init__()
        self.id = feed_id
        self.url = feed_url
        self.stored_update_time: datetime = datetime.fromtimestamp(update_time) if update_time else None
        self.update_time = None
        self.title = None
        self.link = None

    def gather(self):
        feed = feedparser.parse(self.url)
        if feed['bozo'] and not isinstance(feed['bozo_exception'], feedparser.ThingsNobodyCaresAboutButMe)\
                or feed['status'] >= 400:
            raise ex.FeedUnavailable(self.url, feed['status'])
        self.url = feed['href']
        try:
            self.update_time = datetime.fromtimestamp(mktime(feed['feed']['updated_parsed']))
        except KeyError:
            # Sometimes...
            self.update_time = datetime.now()
        self.title = feed['feed']['title']
        self.link = feed['feed']['link']
        self.entries = feed['entries']

    def harvest(self, update_entries: bool = True, max_depth=0):
        super(RssFeed, self).harvest(update_entries=update_entries, max_depth=max_depth)
        
        logger.log('INFO_FEED_HARVEST_END', self.url, self._counts['gathered'], len(self.entries),
                   self._counts['exist'],
                   self._counts['not_supported'], self._counts['errors'], self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['not_supported'],
                   self._inside_counts['errors'])

    def render_for_store(self):
        body = {
            'url': self.url,
            'title': self.title,
            'update_time': self.update_time.timestamp(),
            'link': self.link,
        }
        return body

    def update(self):
        index_storer.update_feed(self.id, self.render_for_store())
        logger.log('INFO_FEED_UPDATE_SUCCESS', self.url)

    def store(self):
        index_storer.store_feed(self.render_for_store())
        logger.log('INFO_FEED_STORE_SUCCESS', self.url)


class UrlFile(UrlList):
    def __init__(self, file_name):
        super(UrlFile, self).__init__()
        with open(file_name, 'r') as f:
            self.entries = f.readlines()


class FeedHarvester:
    def __init__(self):
        self.feeds: List[RssFeed] = []

    def retrieve_feeds(self):
        feeds_dicts = index_searcher.retrieve_feeds_dicts()
        self.feeds = [RssFeed(dic['_source']['url'], dic['_source']['update_time'], dic['_id']) for dic in feeds_dicts]

    def harvest(self, override=False, max_depth=0, delay=0):
        for feed in self.feeds:
            try:
                feed.gather()
                if feed.update_time >= feed.stored_update_time + timedelta(seconds=delay):
                    feed.harvest(update_entries=override, max_depth=max_depth)
                    feed.update()
            except ex.FeedUnavailable:
                continue

    def harvest_feed(self, feed_url, update_entries=True, max_depth=5):
        for feed in self.feeds:
            if feed.url == feed_url:
                feed.gather()
                feed.harvest(update_entries=update_entries, max_depth=max_depth)
                feed.update()
                return
        raise ValueError
