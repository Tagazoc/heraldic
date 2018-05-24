#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module for making graphs.
# Inspired by http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/

from typing import List
from src.store import index_searcher
from collections import defaultdict
from src.misc.functions import get_domain
from src.media.known_media import known_media
from src.misc.exceptions import DomainNotSupportedException, InvalidUrlException
import networkx as net
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np
import math
import pickle


def graph_sources(media_ids: List[str], filename: str):
    try:
        medias_sources = pickle.load(open("save.p", "rb"))
    except FileNotFoundError:
        medias_sources = _get_media_sources(media_ids)

        pickle.dump(medias_sources, open("save.p", "wb"))

    colors = ['red', 'blue', 'green', 'black', 'yellow', 'pink', 'brown', 'purple', 'grey', 'orange',
              'darkblue', 'darkgreen', 'darkred', 'lightblue', 'lightgreen', 'aqua']

    o = net.DiGraph()
    medias_counts = defaultdict(lambda: 0)

    color_index = 0
    for media, sources in medias_sources.items():
        o.add_node(media, color=colors[color_index])
        source_count = 0
        for source, count in sources.items():
            o.add_edge(media, source, count=count, color=colors[color_index])
            source_count += count
        color_index += 1
        medias_counts[media] = source_count

    g = net.DiGraph(net.ego_graph(o, known_media[media_ids[0]].display_name, radius=100))

    # g = _trim_edges(g, weight=1, min_count=1)

    edge_labels = dict([((u, v,), d['count']) for u, v, d in g.edges(data=True)])
    node_colors = [d['color'] for u, d in g.nodes(data=True)]
    pos = net.spring_layout(g, k=1.5)
    # _draw_network(g, pos, ax, edge_labels)
    plt.figure(figsize=(18, 18))
    ns = [math.log10(medias_counts[n] + 1) * 80 for n in g.nodes]
    net.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_size=ns, node_color=node_colors)

    for node, d in g.nodes(data=True):
        node_edges = [(u, v,) for u, v in g.edges() if u == node]
        node_edges_labels = dict([((u, v,), d['count']) for u, v, d in g.edges(data=True) if u == node])
        net.draw_networkx_edges(g, pos, width=0.5, alpha=0.5, edgelist=node_edges, edge_color=d['color'])
        net.draw_networkx_edge_labels(g, pos, edge_labels=node_edges_labels, label_pos=0.4, font_size=10, bbox=dict(alpha=0),
                                      font_color=d['color'])

    plt.axis('off')

    for k in g.nodes:
        x, y = pos[k]
        plt.text(x, y + 0.02, s=k, horizontalalignment='center', fontsize=9)
    plt.savefig(filename)

    plt.show()


def _draw_network(g, pos, ax, labels):

    for n in g:
        c = Circle(pos[n], radius=0.02, alpha=0.5)
        ax.add_patch(c)
        g.node[n]['patch'] = c
        x, y = pos[n]
    seen = {}
    for (u, v, d) in g.edges(data=True):
        n1 = g.node[u]['patch']
        n2 = g.node[v]['patch']
        rad = 0.1
        if (u, v) in seen:
            rad = seen.get((u, v))
            rad = (rad + np.sign(rad)*0.1)*-1
        alpha = 0.5
        color = 'k'

        e = FancyArrowPatch(n1.center, n2.center, patchA=n1, patchB=n2,
                            arrowstyle='-|>',
                            connectionstyle='arc3,rad=%s' % rad,
                            mutation_scale=10.0,
                            lw=2,
                            alpha=alpha,
                            color=color,
                            label=labels[(u, v)])
        seen[(u, v)] = rad
        ax.add_patch(e)


def _get_media_sources(media_ids, include_other_domains=False) -> dict:
    """
    Build a dict with ponderated source domains for each media ; domains from known medias are called by
    their display name.
    :param media_ids: Media IDs
    :return: The dictionary
    """
    medias_sources = {}
    for media_id in media_ids:
        models = index_searcher.search_by_media(media_id, limit=1000)
        display_name = known_media[media_id].display_name

        media_dict = {}
        for model in models:
            for url in model.href_sources.value:
                try:
                    source = get_domain(url)
                except InvalidUrlException:
                    # Invalid URL
                    continue
                try:
                    source = known_media.get_media_by_domain(source, is_subdomain=True).display_name
                except DomainNotSupportedException:
                    if not include_other_domains:
                        continue
                try:
                    media_dict[source] += 1
                except KeyError:
                    media_dict[source] = 1

        medias_sources[display_name] = media_dict
    return medias_sources


def _trim_edges(g, weight=1, min_count=10):
    g2 = net.DiGraph()
    for f, to, edata in g.edges(data=True):
        if edata['count'] >= min_count:
            g2.add_edge(f, to, count=edata['count'])
    return g2
