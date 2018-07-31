#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to analyze document text.
"""

import spacy
from collections import Counter


class TextAnalyzer(object):
    KEPT_TAGS = ['ADJ', 'ADV', 'INTJ', 'NOUN', 'PROPN', 'VERB']
    KEPT_TAGS_MAP = {v: k for k, v in enumerate(KEPT_TAGS)}

    def __init__(self):
        self.nlp = None

    def extract_words(self, text) -> list:
        if self.nlp is None:
            self._load()
        doc = self.nlp(text)
        word_list = [(word.text.lower(), self.KEPT_TAGS_MAP[word.pos_]) for word in doc if word.pos_ in self.KEPT_TAGS]
        counter = Counter(word_list)
        return [(w, p, c) for (w, p), c in counter.items()]

    def _load(self):
        self.nlp = spacy.load('fr_core_news_sm', disable=['parser', 'ner', 'textcat'])


ta = TextAnalyzer()
