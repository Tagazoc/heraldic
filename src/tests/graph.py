#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.analysis import network_graphs


medias_ids = ['liberation', 'le_figaro', '20minutes', 'le_monde']

network_graphs.graph_sources(medias_ids, '/mnt/hgfs/graph.svg')

