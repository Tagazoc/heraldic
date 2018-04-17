#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from src.models.document import Document
from src.misc.exceptions import DocumentExistsException, DomainNotSupportedException, DocumentNotFoundException,\
    DocumentNotChangedException
from src.store import index_storer, index_searcher
from typing import List
from datetime import datetime, timedelta
from time import mktime
from src.misc.logging import logger


class RssFeed:
    def __init__(self, feed_url, update_time=None, feed_id=None):
        self.id = feed_id
        self.url = feed_url
        self.stored_update_time: datetime = datetime.fromtimestamp(update_time) if update_time else None
        self.update_time = None
        self.title = None
        self.link = None
        self.entries = []

    def gather(self):
        feed = feedparser.parse(self.url)

        self.url = feed['href']
        try:
            self.update_time = datetime.fromtimestamp(mktime(feed['feed']['updated_parsed']))
        except KeyError:
            # Sometimes...
            self.update_time = datetime.now()
        self.title = feed['feed']['title']
        self.link = feed['feed']['link']
        self.entries = feed['entries']

    def harvest(self, override: bool=False):
        gather_count = 0
        exists_count = 0
        not_supported_count = 0
        for item in self.entries:
            link = item['link']

            try:
                update_time = datetime.fromtimestamp(mktime(item['updated_parsed']))
            except KeyError:
                update_time = datetime.fromtimestamp(mktime(item['published_parsed']))
            try:
                d = Document(link)
            except DomainNotSupportedException:
                not_supported_count += 1
                continue
            try:

                d.retrieve_from_url()
            except DocumentNotFoundException:
                pass
            try:
                d.gather(update_time=update_time, override=override)
                gather_count += 1
            except DocumentExistsException:
                exists_count += 1
            except DocumentNotChangedException:
                exists_count += 1
            except DomainNotSupportedException:
                not_supported_count += 1
        logger.log('INFO_FEED_HARVEST_END', self.url, gather_count, len(self.entries), exists_count, not_supported_count)

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


class FeedHarvester:
    def __init__(self):
        self.feeds: List[RssFeed] = []

    def retrieve_feeds(self):
        feeds_dicts = index_searcher.retrieve_feeds_dicts()
        self.feeds = [RssFeed(dic['_source']['url'], dic['_source']['update_time'], dic['_id']) for dic in feeds_dicts]

    def harvest(self, override=False, delay=0):
        for feed in self.feeds:
            feed.gather()
            if feed.update_time >= feed.stored_update_time + timedelta(seconds=delay):
                feed.harvest(override=override)
                feed.update()

    def harvest_feed(self, feed_url, override=False):
        for feed in self.feeds:
            if feed.url == feed_url:
                feed.gather()
                feed.harvest(override=override)
                feed.update()
                return
        raise ValueError
