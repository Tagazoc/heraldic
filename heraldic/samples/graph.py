#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heraldic.analysis import network_graphs
from heraldic.media.known_media import known_media


medias_ids = known_media.names  # ['liberation', 'le_figaro', '20minutes', 'le_monde']

# network_graphs.graph_sources(medias_ids, '/mnt/hgfs/graph2.svg')
network_graphs.graph_media_sources('le_figaro', '/mnt/hgfs/liberation.svg', 1)

