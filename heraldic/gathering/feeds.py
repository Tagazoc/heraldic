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
    def __init__(self, entries=None):
        
        self.gathered_urls = set()
        self.entries = list(entries) if entries is not None else []
        self.last_update_time: datetime = None

        self._counts = {
            'gathered': 0,
            'exist': 0,
            'domain_not_supported': 0,
            'url_not_supported': 0,
            'errors': 0
        }

        self._inside_counts = {
            'gathered': 0,
            'total': 0,
            'exist': 0,
            'domain_not_supported': 0,
            'url_not_supported': 0,
            'errors': 0
        }

    def harvest(self, update_entries=True, max_depth=0, raise_on_optional=False, dump_result=False):
        self._gather_links(self.entries, update_entries=update_entries, max_depth=max_depth,
                           raise_on_optional=raise_on_optional, dump_result=dump_result)

        logger.log('INFO_LIST_HARVEST_END', self._counts['gathered'], len(self.entries),
                   self._counts['exist'], self._counts['domain_not_supported'],
                   self._counts['url_not_supported'], self._counts['errors'], self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['domain_not_supported'],
                   self._inside_counts['url_not_supported'], self._inside_counts['errors'])

    def _gather_links(self, items: List, update_entries=False, max_depth=0, depth=0, raise_on_optional=False,
                      dump_result=False):
        counts = self._counts if depth == 0 else self._inside_counts
        for item in items:

            try:
                # items are feed entries
                url = item['link']
                try:
                    update_time = datetime.fromtimestamp(mktime(item['updated_parsed']))
                except TypeError:
                    update_time = None
            except KeyError:
                try:
                    update_time = datetime.fromtimestamp(mktime(item['published_parsed']))
                except KeyError:
                    update_time = None
            except TypeError:
                # items are only links
                url = item
                update_time = None

            # Unless an update is enforced, entries which did not change since last feed update are skipped
            if not update_entries and self.last_update_time is not None and update_time is not None \
                    and self.last_update_time >= update_time:
                counts['exist'] += 1
                continue

            d = None
            try:
                protocol, url = get_truncated_url(url)
                if url in self.gathered_urls:
                    continue
                self.gathered_urls = self.gathered_urls.union([url])
                d = Document(protocol + url)
                d.gather(update_time=update_time, update=update_entries, raise_on_optional=raise_on_optional)
                if dump_result:
                    print(str(d))
                self.gathered_urls = self.gathered_urls.union(d.model.urls.value)
                counts['gathered'] += 1
            except ex.UrlNotSupportedException:
                counts['url_not_supported'] += 1
                continue
            except ex.DomainNotSupportedException:
                counts['domain_not_supported'] += 1
                continue
            except ex.GatherError:
                counts['errors'] += 1
                if raise_on_optional:
                    raise
                continue
            except ConnectionError:
                counts['errors'] += 1
                continue
            except RequestException:
                counts['errors'] += 1
                continue
            # If document is already up-to-date, still gather inside links
            except ex.DocumentExistsException:
                counts['exist'] += 1

            if max_depth > depth:
                inside_links = d.model.href_sources.value + d.model.side_links.value
                self._inside_counts['total'] += len(inside_links)
                # Gather internal links, but without updating existing documents
                self._gather_links(inside_links, update_entries=update_entries, max_depth=max_depth, depth=depth + 1)


class RssFeed(UrlList):
    def __init__(self, feed_url, media_id=None, last_update_time=None, feed_id=None):
        super(RssFeed, self).__init__()
        self.id = feed_id
        self.url = feed_url
        self.last_update_time: datetime = datetime.fromtimestamp(last_update_time) if last_update_time else None
        self.update_time = None
        self.title = None
        self.link = None
        self.media_id = media_id

    def gather(self):
        feed = feedparser.parse(self.url)
        if feed['status'] >= 400 or (feed['bozo']
                                     and not isinstance(feed['bozo_exception'], feedparser.CharacterEncodingOverride)
                                     and not isinstance(feed['bozo_exception'], feedparser.ThingsNobodyCaresAboutButMe)
                                     ):  # And me.
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

    def harvest(self, update_entries: bool = True, max_depth=0, raise_on_optional=False, dump_result=False):
        self._gather_links(self.entries, update_entries=update_entries, max_depth=max_depth,
                           raise_on_optional=raise_on_optional, dump_result=dump_result)

        logger.log('INFO_FEED_HARVEST_END', self.url, self._counts['gathered'], len(self.entries),
                   self._counts['exist'],
                   self._counts['domain_not_supported'], self._counts['url_not_supported'],
                   self._counts['errors'], self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['domain_not_supported'],
                   self._inside_counts['domain_not_supported'], self._inside_counts['errors'])

    def render_for_store(self):
        body = {
            'url': self.url,
            'title': self.title,
            'update_time': self.update_time.timestamp(),
            'link': self.link,
            'media_id': self.media_id
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
        with open(file_name, 'r') as f:
            super(UrlFile, self).__init__(f.read().splitlines())


class FeedHarvester:
    def __init__(self):
        self.feeds: List[RssFeed] = []

    def retrieve_feeds(self, media_id=None):
        feeds_dicts = index_searcher.retrieve_feeds_dicts()
        if media_id is not None:
            feeds_dicts = [dic for dic in feeds_dicts if dic['_source']['media_id'] == media_id]
        self.feeds = [RssFeed(dic['_source']['url'], dic['_source']['media_id'],
                              dic['_source']['update_time'], dic['_id']) for dic in feeds_dicts]

    def harvest(self, override=False, max_depth=0, delay=0):
        for feed in self.feeds:
            try:
                feed.gather()
                if feed.update_time >= feed.last_update_time + timedelta(seconds=delay):
                    feed.harvest(update_entries=override, max_depth=max_depth)
                    feed.update()
            except ex.FeedUnavailable:
                continue

    @staticmethod
    def harvest_feed(feed_url, update_entries=True, max_depth=5):
        feed = RssFeed(feed_url)
        feed.gather()
        feed.harvest(update_entries=update_entries, max_depth=max_depth)
