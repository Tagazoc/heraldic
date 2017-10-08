#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used to analyze document text.
"""

import nltk
from collections import Counter
import unicodedata
import re
import spacy
from spacy.fr import FrenchDefaults
from spacy.lemmatizerlookup import Lemmatizer
from nltk.tag import StanfordPOSTagger
from nltk.stem import SnowballStemmer
import os


class TextAnalyzer(object):
    def __init__(self, text):
        # TODO
        pass
        # punctuation_signs = ''.join(chr(x) for x in range(65536) if unicodedata.category(chr(x)).startswith('P'))
        # punctuation_re = re.compile('[' + punctuation_signs + ']')

        # tokens_without_punctuation = [token for token in tokens if not punctuation_re.match(token)]
        # self.nlp = spacy.load('fr')

        # self._tokenize(text)
        # self._pos_tag()
        # self._lemmatize()

    def _tokenize(self, text):
        self.doc = self.nlp(text)

    def _pos_tag(self):
        for word in self.doc:
            print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

        # lib_stanford_pos = 'lib/stanford-postagger-full/'

        # jar = lib_stanford_pos + 'stanford-postagger-3.8.0.jar'

        # model = lib_stanford_pos + 'models/french.tagger'


        # java_path = "/usr/lib/jvm/java-8-openjdk/jre/bin/java"

        # os.environ['JAVAHOME'] = java_path


        # pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

        # res = pos_tagger.tag(self.tokens)

        # print(res)

    def _lemmatize(self):
        l = Lemmatizer('/home/f/PycharmProjects/heraldic/lemmatization-fr.txt')
