#!/usr/bin/env python
# -*- coding: utf-8 -*-

import feedparser
from src.models.document import Document
from src.heraldic_exceptions import DocumentExistsException
from src.store import model_storer, model_searcher


class RssFeed:
    def __init__(self, feed_url, version=None, feed_id=None):
        self.id = feed_id
        self.stored_version = version
        self.url = feed_url
        self.current_version = None
        self.title = None
        self.description = None
        self.link = None
        self.items = []

    def gather(self):
        feed = feedparser.parse(self.url)

        self.url = feed['url']
        self.current_version = feed['version']
        self.title = feed['channel']['title']
        self.description = feed['channel']['description']
        self.link = feed['channel']['link']
        self.items = feed['items']

    def harvest(self):
        for item in self.items:
            d = Document()
            try:
                d.gather(item['link'])
                d.store()
            except DocumentExistsException:
                pass

    def render_for_store(self):
        body = {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'link': self.link,
            'version': self.current_version
        }
        return body

    def update(self):
        model_storer.update_feed(self.id, self.render_for_store())

    def store(self):
        model_storer.store_feed(self.render_for_store())
