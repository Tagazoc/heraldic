#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for drawing word clouds.
"""

import matplotlib.pyplot as plt
from heraldic.models.document_model import DocumentModel
from typing import List
import heraldic.store.index_searcher as i_s
from wordcloud import WordCloud
from heraldic.media.known_media import known_media


def generate_media_word_cloud(media_id):
    models = i_s.search_by_media(media_id, limit=10000)
    text = _generate_text_from_models(models)

    wordcloud = WordCloud(collocations=False).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def generate_multiple_media_word_cloud(media_ids: List[str]):
    text = ''
    for media_id in media_ids:
        models = i_s.search_by_media(media_id, limit=10000)
        text += _generate_text_from_models(models)

    wordcloud = WordCloud(collocations=False).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def _generate_text_from_models(models: List[DocumentModel]):
    word_dict = {}
    for model in models:
        for word, pos, count in model.words.value:
            try:
                word_dict[word, pos] += count
            except KeyError:
                word_dict[word, pos] = count
    text = ''
    for (word, pos), count in word_dict.items():
        text += (word + ' ') * count
    return text


generate_multiple_media_word_cloud(known_media.names)
