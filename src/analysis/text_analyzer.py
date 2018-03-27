#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to analyze document text.
"""

import spacy


class TextAnalyzer(object):
    def __init__(self):
        self.nlp = spacy.load('fr_core_news_sm')

    def analyze(self, text):
        self._tokenize(text)
        self._pos_tag()
        self._lemmatize()

    def _tokenize(self, text):
        self.doc = self.nlp(text)

    def _pos_tag(self):
        for word in self.doc:
            print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

    def _lemmatize(self):
        pass
        # l = Lemmatizer('/home/f/PycharmProjects/heraldic/lemmatization-fr.txt')


ta = TextAnalyzer()
