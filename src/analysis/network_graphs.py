#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module for making graphs.
# Inspired by http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/

from typing import List
from src.models import model_searcher
from collections import defaultdict
from src.misc.functions import get_domain
from src.media.known_media import known_media
from src.misc.exceptions import DomainNotSupportedException
import networkx as net
import matplotlib.pyplot as plt
import math


def graph_sources(media_ids: List[str], filename: str):
    medias_sources = _get_media_sources(media_ids)

    o = net.DiGraph()
    medias_counts = defaultdict(lambda: 0)
    for media, sources in medias_sources.items():
        source_count = 0
        for source, count in sources.items():
            o.add_edge(media, source, count=count)
            source_count += count
        medias_counts[media] = source_count

    g = net.DiGraph(net.ego_graph(o, known_media[media_ids[0]].display_name, radius=4))
    g = _trim_edges(g, weight=1, min_count=2)
    pos = net.spring_layout(g, k=1)

    plt.figure(figsize=(18, 18))
    plt.axis('off')
    ns = [math.log10(medias_counts[n] + 1) * 80 for n in g.nodes]
    net.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_size=ns)

    net.draw_networkx_edges(g, pos, width=0.5, alpha=0.5)
    edge_labels = dict([((u, v,), d['count'])
                        for u, v, d in g.edges(data=True)])
    net.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=6, bbox=dict(alpha=0))
    for k in g.nodes:
        x, y = pos[k]
        plt.text(x, y + 0.02, s=k, horizontalalignment='center', fontsize=9)
    plt.savefig(filename)


def _get_media_sources(media_ids) -> dict:
    medias_sources = {}
    for media_id in media_ids:
        models = model_searcher.search_by_media(media_id, limit=1000)
        display_name = known_media[media_id].display_name

        media_dict = defaultdict(lambda: 0)
        for model in models:
            for url in model.href_sources.value:
                try:
                    source = get_domain(url)
                except ValueError:
                    # Invalid URL
                    continue
                try:
                    source = known_media.get_media_by_domain(source).display_name
                except DomainNotSupportedException:
                    pass

                media_dict[source] += 1

        medias_sources[display_name] = media_dict
    return medias_sources


def _trim_edges(g, weight=1, min_count=10):
    g2 = net.DiGraph()
    for f, to, edata in g.edges(data=True):
        if edata['count'] >= min_count:
            g2.add_edge(f, to, count=edata['count'])
    return g2
