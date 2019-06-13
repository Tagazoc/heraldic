#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from heraldic.models.document import Document
import heraldic.misc.exceptions as ex
from heraldic.store import index_storer, index_searcher
from typing import List
from datetime import datetime, timedelta
from time import mktime, sleep
from heraldic.misc.logging import logger
from heraldic.misc.functions import get_truncated_url, get_domain
from requests.exceptions import RequestException
from heraldic.media.known_media import known_media


class UrlList:
    def __init__(self, entries=None, **kwargs):
        
        self.known_urls = set()
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
        self.crawl_delay = kwargs['crawl_delay'] if 'crawl_delay' in kwargs else 0
        self.crawl_domains = kwargs['crawl_domains'] if 'crawl_domains' in kwargs else None
        self.update_inplace = kwargs['update_inplace'] if 'update_inplace' in kwargs else True
        self.max_depth = kwargs['max_depth'] if 'max_depth' in kwargs else False
        self.raise_on_optional = kwargs['raise_on_optional'] if 'raise_on_optional' in kwargs else False
        self.dump_result = kwargs['dump_result'] if 'dump_result' in kwargs else False

    def harvest(self):
        self._gather_links(self.entries)

        logger.log('INFO_LIST_HARVEST_END', self._counts['gathered'], self._counts['total'],
                   self._counts['exist'], self._counts['domain_not_supported'],
                   self._counts['url_not_supported'], self._counts['not_article'], self._counts['errors'],
                   self._inside_counts['gathered'],
                   self._inside_counts['total'], self._inside_counts['exist'], self._inside_counts['domain_not_supported'],
                   self._inside_counts['url_not_supported'], self._inside_counts['not_article'], self._inside_counts['errors'])

    def _gather_links(self, items: List, depth=0):
        counts = self._counts if depth == 0 else self._inside_counts
        for item in items:
            if self.crawl_delay:
                sleep(self.crawl_delay)
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
            if not self.update_inplace and self.last_update_time is not None and update_time is not None \
                    and self.last_update_time >= update_time:
                counts['exist'] += 1
                continue

            d = None
            try:
                protocol, url = get_truncated_url(url)
                if url in self.known_urls:
                    continue
                self.known_urls = self.known_urls.union([url])
                d = Document(protocol + url)
                d.gather(update_time=update_time, update_inplace=self.update_inplace, raise_on_optional=self.raise_on_optional)
                self.known_urls = self.known_urls.union(d.model.urls.value)
                counts['gathered'] += 1
            # If document is already up-to-date, still gather inside links
            except ex.DocumentExistsException:
                counts['exist'] += 1
            except (ex.GatherException, ConnectionError, RequestException) as e:
                self._handle_error_counts(counts, e)
                continue

            if self.dump_result:
                print(str(d))

            if self.max_depth > depth:
                inside_links = d.model.href_sources.value + d.model.side_links.value
                if self.crawl_domains is not None:
                    inside_links = [link for link in inside_links if get_domain(link) in self.crawl_domains]
                self._inside_counts['total'] += len(inside_links)
                # Gather internal links, but without updating existing documents
                self._gather_links(inside_links, depth=depth + 1)

    def _handle_error_counts(self, counts: List, e: Exception):
        if isinstance(e, ex.UrlNotSupportedException):
            counts['url_not_supported'] += 1
        elif isinstance(e, ex.DomainNotSupportedException):
            counts['domain_not_supported'] += 1
        elif isinstance(e, ex.DocumentNotArticleException):
            counts['not_article'] += 1
        elif isinstance(e, ex.GatherError):
            counts['errors'] += 1
            if self.raise_on_optional:
                raise e
        elif isinstance(e, ConnectionError):
            counts['errors'] += 1
        elif isinstance(e, RequestException):
            counts['errors'] += 1


class RssFeed(UrlList):
    def __init__(self, feed_url, media_id=None, last_update_time=None, feed_id=None, **kwargs):
        self.id = feed_id
        self.url = feed_url
        self.title = ''
        self.link = feed_url
        self.media_id = media_id
        self.media_domains = known_media[media_id].supported_domains if media_id is not None else None

        crawl_domains = self.media_domains if 'crawl_internally' in kwargs and kwargs['crawl_internally'] else None
        kwargs['crawl_domains'] = crawl_domains
        super(RssFeed, self).__init__(**kwargs)

        self.last_update_time: datetime = datetime.fromtimestamp(last_update_time) if last_update_time else None
        self.update_time = None

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
        except (KeyError, TypeError):
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

    def harvest(self):
        self._gather_links(self.entries)

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
    def __init__(self, file_name, **kwargs):
        with open(file_name, 'r') as f:
            super(UrlFile, self).__init__(f.read().splitlines(), **kwargs)


class FeedHarvester:
    def __init__(self, **kwargs):
        self.feeds: List[RssFeed] = []
        self.kwargs = kwargs

    def retrieve_feeds(self, media_id=None):
        feeds_dicts = index_searcher.retrieve_feeds_dicts()
        if media_id is not None:
            feeds_dicts = [dic for dic in feeds_dicts if dic['_source']['media_id'] == media_id]
        self.feeds = [RssFeed(dic['_source']['url'], dic['_source']['media_id'],
                              dic['_source']['update_time'], dic['_id'], **self.kwargs) for dic in feeds_dicts]

    def harvest(self, delay=0):
        for feed in self.feeds:
            try:
                feed.gather()
                if feed.update_time >= feed.last_update_time + timedelta(seconds=delay):
                    feed.harvest()
                    feed.update()
            except ex.FeedUnavailable:
                continue


class SourceHarvester(UrlList):
    def __init__(self, media_id, **kwargs):

        self.media_id = media_id
        self.media_domains = known_media[media_id].supported_domains if media_id is not None else None
        crawl_domains = self.media_domains if 'crawl_internally' in kwargs and kwargs['crawl_internally'] else None
        kwargs['crawl_domains'] = crawl_domains
        super(SourceHarvester, self).__init__(**kwargs)
        self.recursive_step = kwargs['recursive_step'] if 'recursive_step' in kwargs else 0
        self.sources_only = kwargs['sources_only'] if 'sources_only' in kwargs else False
        self.source_gathered_urls = []

    def harvest(self):
        if self.media_id is not None:
            docs = index_searcher.search_by_media(self.media_id)
        else:
            docs = index_searcher.search_models()
        source_harvest_count = 0
        for doc in docs:
            urls = doc.href_sources.value if self.sources_only else [doc.urls.value[0]]
            for url in urls:
                to_gather = False  # Come togather
                if url not in self.known_urls:
                    if self.crawl_domains is None or get_domain(url, do_not_log=True) in self.crawl_domains:
                        try:
                            model = index_searcher.search_model_by_url(url)
                            self.known_urls = self.known_urls.union(model.urls.value)
                        except ex.DocumentNotFoundException:
                            to_gather = True  # Right now
                        if to_gather or not self.sources_only:  # Over me.
                            d = Document(url)
                            try:
                                d.gather()
                                self._counts['gathered'] += 1
                            except (ex.GatherException, ConnectionError, RequestException) as e:
                                self._handle_error_counts(self._counts, e)
                                continue

                            if self.dump_result:
                                print(str(d))

                            self.source_gathered_urls.extend(d.model.href_sources.value)
                            self.source_gathered_urls.extend(d.model.side_links.value)
                            self.known_urls = self.known_urls.union(d.model.urls.value)
                            source_harvest_count += 1

                            if self.crawl_delay:
                                sleep(self.crawl_delay)

                            if self.max_depth > 0:
                                if self.recursive_step == 0 or source_harvest_count % self.recursive_step == 0:
                                    self._gather_links(self.source_gathered_urls, depth=1)
                                    self.source_gathered_urls = []
                else:
                    self.known_urls = self.known_urls.union(url)


class ErrorHarvester(SourceHarvester):
    def __init__(self, media_id, **kwargs):
        super(ErrorHarvester, self).__init__(media_id, **kwargs)

        self.error_attribute = kwargs['error_attribute'] if 'error_attribute' in kwargs else None
        self.error_body = kwargs['error_body'] if 'error_body' in kwargs else None

    def harvest(self):
        urls = index_searcher.get_similar_errors_urls(self.media_id, self.error_attribute, self.error_body)
        source_harvest_count = 0
        for url in urls:
            if url not in self.known_urls:
                if self.crawl_domains is None or get_domain(url, do_not_log=True) in self.crawl_domains:
                    d = Document(url)
                    try:
                        d.gather()
                        self._counts['gathered'] += 1
                    except (ex.GatherException, ConnectionError, RequestException) as e:
                        self._handle_error_counts(self._counts, e)
                        continue

                    if self.dump_result:
                        print(str(d))

                    self.source_gathered_urls.extend(d.model.href_sources.value)
                    self.source_gathered_urls.extend(d.model.side_links.value)
                    self.known_urls = self.known_urls.union(d.model.urls.value)
                    source_harvest_count += 1

                    if self.crawl_delay:
                        sleep(self.crawl_delay)

                    if self.max_depth > 0:
                        if self.recursive_step == 0 or source_harvest_count % self.recursive_step == 0:
                            self._gather_links(self.source_gathered_urls, depth=1)
                            self.source_gathered_urls = []
