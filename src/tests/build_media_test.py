#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module used to create test files from a stored document.
"""

from src.models.document import Document


url = 'http://www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute' \
      '-lrem_1593251'

d = Document()
d.retrieve_from_url(url)

doc_dict_content = 'doc_dict = { \n'

for k, v in d.model.attributes.items():
    if v.storable:
        doc_dict_content += '    "' + k + '": "' + v.render_for_display() + '",\n'

doc_dict_content = doc_dict_content[:-2] + "\n"
doc_dict_content += '}'

sugg_dict_content = 'suggestion_dict = { \n'

for k, v in d.model.attributes.items():
    if v.suggestions:
        sugg_dict_content += '    "' + k + '": [\n        "' +\
                             '",\n        "'.join(v.render_suggestions_for_display()) + '"\n    ],\n'

sugg_dict_content = sugg_dict_content[:-2] + "\n"
sugg_dict_content += '}'


print(doc_dict_content)
print(sugg_dict_content)
