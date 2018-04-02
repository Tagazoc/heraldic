#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file can be used as a script to validate parsing of an article.
"""

from src.models.document import Document
import sys
from bs4 import BeautifulSoup

url = sys.argv[1]

d = Document()
d.model.gather_from_url(url)
bs = BeautifulSoup(d.model.content.render_for_display(), "html.parser")
