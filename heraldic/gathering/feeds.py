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
from heraldic.misc.functions import get_truncated_url, get_domain
from requests.exceptions import RequestException
from heraldic.media.known_media import known_media


class UrlList:
    def __init__(self, entries=None):
        
        self.gathered_urls = set()
        self.entries = entries if entries is not None else []
        self.last_update_time: datetime = None

        self._counts = {
            'gathered': 0,
            'exist': 0,
            'domain_not_supported': 0,
            'url_not_supported': 0,
            'not_article': 0,
            'errors': 0,
            'total': 0
        }

        self._inside_counts = {
            'gathered': 0,
            'total': 0,
            'exist': 0,
            'domain_not_supported': 0,
            'url_not_supported': 0,
            'not_article': 0,
            'errors': 0
        }

    def harvest(self, update_inplace=True, max_depth=0, raise_on_optional=False, dump_result=False):
        self._gather_links(self.entries, update_inplace=update_inplace, max_depth=max_depth,
                           raise_on_optional=raise_on_optional, dump_result=dump_result)

        logger.log('INFO_LIST_HARVEST_END', self._counts['gathered'], self._counts['total'],
                   self._counts['exist'], self._counts['domain_not_supported'],
                   self._counts['url_not_supported'], self._counts['not_article'], self._counts['errors'],
                   self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['domain_not_supported'],
                   self._inside_counts['url_not_supported'], self._inside_counts['not_article'], self._inside_counts['errors'])

    def _gather_links(self, items: List, update_inplace=False, max_depth=0, depth=0, raise_on_optional=False,
                      dump_result=False, restricted_crawl_domains=None):
        counts = self._counts if depth == 0 else self._inside_counts
        for item in items:
            self._counts['total'] += 1
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
            if not update_inplace and self.last_update_time is not None and update_time is not None \
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
                d.gather(update_time=update_time, update_inplace=update_inplace, raise_on_optional=raise_on_optional)
                self.gathered_urls = self.gathered_urls.union(d.model.urls.value)
                counts['gathered'] += 1
            except ex.UrlNotSupportedException:
                counts['url_not_supported'] += 1
                continue
            except ex.DomainNotSupportedException:
                counts['domain_not_supported'] += 1
                continue
            except ex.DocumentNotArticleException:
                counts['not_article'] += 1
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

            if dump_result:
                print(str(d))

            if max_depth > depth:
                inside_links = d.model.href_sources.value + d.model.side_links.value
                if restricted_crawl_domains is not None:
                    inside_links = [link for link in inside_links if get_domain(link) in restricted_crawl_domains]
                self._inside_counts['total'] += len(inside_links)
                # Gather internal links, but without updating existing documents
                self._gather_links(inside_links, update_inplace=update_inplace, max_depth=max_depth, depth=depth + 1,
                                   restricted_crawl_domains=restricted_crawl_domains)


class RssFeed(UrlList):
    def __init__(self, feed_url, media_id=None, last_update_time=None, feed_id=None):
        super(RssFeed, self).__init__()
        self.id = feed_id
        self.url = feed_url
        self.last_update_time: datetime = datetime.fromtimestamp(last_update_time) if last_update_time else None
        self.update_time = None
        self.title = ''
        self.link = feed_url
        self.media_id = media_id
        self.media_domains = known_media[media_id].supported_domains

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
        try:
            self.title = feed['feed']['title']
        except KeyError:
            pass
        try:
            self.link = feed['feed']['link']
        except KeyError:
            pass
        self.entries = feed['entries']

    def harvest(self, update_inplace: bool = True, max_depth=0, raise_on_optional=False, dump_result=False, crawl_internally=False):
        only_domains = self.media_domains if crawl_internally else None
        self._gather_links(self.entries, update_inplace=update_inplace, max_depth=max_depth,
                           raise_on_optional=raise_on_optional, dump_result=dump_result, restricted_crawl_domains=only_domains)

        logger.log('INFO_FEED_HARVEST_END', self.url, self._counts['gathered'], self._counts['total'],
                   self._counts['exist'],
                   self._counts['domain_not_supported'], self._counts['url_not_supported'], self._counts['not_article'],
                   self._counts['errors'], self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['domain_not_supported'],
                   self._inside_counts['domain_not_supported'], self._inside_counts['not_article'], self._inside_counts['errors'])

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

    def harvest(self, override=False, max_depth=0, delay=0, crawl_internally=False):
        for feed in self.feeds:
            try:
                feed.gather()
                if feed.update_time >= feed.last_update_time + timedelta(seconds=delay):
                    feed.harvest(update_inplace=override, max_depth=max_depth, crawl_internally=crawl_internally)
                    feed.update()
            except ex.FeedUnavailable:
                continue

    @staticmethod
    def harvest_feed(feed_url, update_entries=True, max_depth=5):
        feed = RssFeed(feed_url)
        feed.gather()
        feed.harvest(update_inplace=update_entries, max_depth=max_depth)
