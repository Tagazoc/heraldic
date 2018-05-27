#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Module for making graphs.
# Inspired by http://mark-kay.net/2014/08/15/network-graph-of-twitter-followers/

from typing import List
from src.store import index_searcher
from collections import defaultdict
from src.misc.functions import get_domain, get_truncated_url
from src.media.known_media import known_media
import src.misc.exceptions as ex
import networkx as net
import matplotlib.pyplot as plt
import math
import pickle


def graph_media_sources(media_id: str, filename: str, depth=0, min_count=0):
    media_name = known_media[media_id].display_name

    # Have data been previously saved ?
    try:
        source_tree = pickle.load(open("graph_sources_" + media_id + ".p", "rb"))
    except FileNotFoundError:
        # Get all documents for this media
        source_tree = {}
        models = index_searcher.search_by_media(media_id, limit=5000)
        # Build source tree with dicts within dicts
        for model in models:
            source_tree = _merge_url_dicts(source_tree,
                                           _retrieve_recursive_sources(model, include_other_domains=True,
                                                                       depth=depth,
                                                                       initial_media_name=media_name))

        pickle.dump(source_tree, open("graph_sources_" + media_id + ".p", "wb"))

    o = net.DiGraph()
    o.add_node(media_name, media=True)
    # Add nodes and edges from our source tree
    _graph_from_recursive_sources(o, media_name, source_tree)

    # Trim too small edges
    o = _trim_edges(o, min_count=min_count)

    # Ego graph with shell layout, supported media in inner circle
    g = net.ego_graph(o, media_name, radius=5)
    nlist = [[media_name], [n for n, d in g.nodes(data=True) if d['media'] and n != media_name],
             [n for n, d in g.nodes(data=True) if not d['media']]]
    pos = net.shell_layout(g, nlist)

    # Set node colors, edge labels and edges colors
    color_map = {True: 'red', False: 'blue'}
    size_map = {True: 150, False: 35}
    node_colors = [color_map[d['media']] for u, d in g.nodes(data=True)]
    node_sizes = [size_map[d['media']] for u, d in g.nodes(data=True)]
    edge_color_indexes = [d['count'] for u, v, d in g.edges(data=True)]
    edge_labels = dict([((u, v,), d['count']) for u, v, d in g.edges(data=True)])

    # Draw
    plt.figure(figsize=(18, 18))
    net.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_color=node_colors, node_size=node_sizes, alpha=0.5)
    net.draw_networkx_edges(g, pos, width=3, alpha=0.5,
                            edgelist=g.edges(), edge_cmap=plt.get_cmap(plt.get_cmap('Blues')),
                            edge_color=edge_color_indexes, edge_vmin=-10, edge_vmax=max(edge_color_indexes))

    net.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, label_pos=0.4, font_size=10,
                                  bbox=dict(boxstyle='round', alpha=0.3, fc='white', ec='white'))
    plt.axis('off')

    # Node legends
    for k in g.nodes:
        x, y = pos[k]
        plt.text(x, y + 0.02, s=k, horizontalalignment='center', fontsize=9)
    plt.savefig(filename)

    plt.show()


def graph_multiple_sources(media_ids: List[str], filename: str):
    try:
        medias_sources = pickle.load(open("save.p", "rb"))
    except FileNotFoundError:
        medias_sources = _get_media_sources(media_ids)

        pickle.dump(medias_sources, open("save.p", "wb"))

    cmaps = [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds'
    ]
    colors = ['black', 'purple', 'blue', 'green', 'orange', 'red',
              'black', 'purple', 'blue', 'green', 'orange', 'red',
              'black', 'purple', 'blue', 'green', 'orange', 'red'
              ]

    g = net.DiGraph()
    medias_counts = defaultdict(lambda: 0)

    color_index = 0
    max_sources = 0
    for media, (sources, doc_count) in medias_sources.items():
        g.add_node(media, color=color_index)
        source_count = 0
        for source, count in sources.items():
            g.add_edge(media, source, count=count, color=color_index)
            source_count += count
            if source != media:
                max_sources = max(max_sources, count)
        color_index += 1
        medias_counts[media] = (doc_count, source_count)

    g = _trim_edges(g, min_count=5)

    node_colors = [colors[d['color']] for u, d in g.nodes(data=True)]

    pos = net.circular_layout(g, 5)

    plt.figure(figsize=(18, 18))
    ns = [math.log10(medias_counts[n][0] + 1) * 80 for n in g.nodes]
    net.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_size=ns, node_color=node_colors, alpha=0.5)

    for node, d in g.nodes(data=True):
        node_edges = [(u, v,) for u, v in g.edges() if u == node]
        edge_color_indexes = [d['count'] for (u, v, d) in g.edges(data=True) if u == node]
        node_edges_labels = dict([((u, v,), d['count']) for u, v, d in g.edges(data=True) if u == node])
        net.draw_networkx_edges(g, pos, width=3, alpha=0.5,
                                edgelist=node_edges, edge_cmap=plt.get_cmap(cmaps[d['color']]),
                                edge_color=edge_color_indexes, edge_vmin=0, edge_vmax=max_sources)
        net.draw_networkx_edge_labels(g, pos, edge_labels=node_edges_labels, label_pos=0.7, font_size=10,
                                      bbox=dict(boxstyle='round', alpha=0.3, fc='white', ec='white'),
                                      font_color=colors[d['color']])

    plt.axis('off')

    for k in g.nodes:
        x, y = pos[k]
        plt.text(x, y + 0.2, s=k + ' (' + str(medias_counts[k][0]) + ')', horizontalalignment='center', fontsize=9)
    plt.savefig(filename)

    plt.show()


def _retrieve_recursive_sources(model, include_other_domains=False, depth=0, initial_media_name=None) -> dict:
    # dict domain > dict (dict( {}, count), count), count
    # libé : {marianne: (mrm: {}, 4), 7}, 18
    model_dict = {}
    for url in model.href_sources.value:
        try:
            source = get_domain(url)
        except ex.InvalidUrlException:
            # Invalid URL
            continue
        url_dict = {}
        try:
            source = known_media.get_media_by_domain(source, is_subdomain=True, log_failure=False).display_name

            if initial_media_name == source:
                continue
            url_doc = index_searcher.retrieve_model_from_url(get_truncated_url(url))
            if depth > 0:
                url_dict = _retrieve_recursive_sources(url_doc, include_other_domains, depth - 1, initial_media_name)
        except ex.DomainNotSupportedException:
            if not include_other_domains:
                continue
        except ex.DocumentNotFoundException:
            pass
        try:
            model_dict[source] = (_merge_url_dicts(model_dict[source][0], url_dict), model_dict[source][1] + 1)
        except KeyError:
            model_dict[source] = (url_dict, 1)
    return model_dict


def _graph_from_recursive_sources(g, origin_domain, source_dict):
    for domain, (_dict, count) in source_dict.items():
        if domain not in g.nodes():
            media = True if _dict else False

            g.add_node(domain, media=media, count=count)

        g.add_edge(origin_domain, domain, count=count)
        _graph_from_recursive_sources(g, domain, _dict)


def _merge_url_dicts(a: dict, b: dict) -> dict:
    if a == {} or b == {}:
        return a or b
    c = {}
    for media, (inner_dict, count) in a.items():
        if media in b.keys():
            c[media] = (_merge_url_dicts(inner_dict, b[media][0]), count + b[media][1])
            del b[media]
        else:
            c[media] = (inner_dict, count)
    for media, (inner_dict, count) in b.items():
        c[media] = (inner_dict, count)
    return c


def _get_media_sources(media_ids, include_other_domains=False) -> dict:
    """
    Build a dict with ponderated source domains for each media ; domains from known medias are called by
    their display name.
    :param media_ids: Media IDs
    :return: The dictionary
    """
    medias_sources = {}
    for media_id in media_ids:
        models = index_searcher.search_by_media(media_id, limit=5000)
        display_name = known_media[media_id].display_name

        media_dict = {}
        for model in models:
            for url in model.href_sources.value:
                try:
                    source = get_domain(url)
                except ex.InvalidUrlException:
                    # Invalid URL
                    continue
                try:
                    source = known_media.get_media_by_domain(source, is_subdomain=True, log_failure=False).display_name
                except ex.DomainNotSupportedException:
                    if not include_other_domains:
                        continue
                try:
                    media_dict[source] += 1
                except KeyError:
                    media_dict[source] = 1

        medias_sources[display_name] = (media_dict, len(models))
    return medias_sources


def _trim_edges(g, min_count=10):
    g2 = net.DiGraph()
    for n, edata in g.nodes(data=True):
        g2.add_node(n, **edata)
    for f, to, edata in g.edges(data=True):
        if edata['count'] >= min_count:
            g2.add_edge(f, to, **edata)
    return g2
