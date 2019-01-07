#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script generates a yaml representation of document model.
"""

from heraldic.models.document_model import DocumentModel
import yaml

model = DocumentModel()
yaml_definition = {k: {**v.OPENAPI_SCHEMA, **{'description': v.desc}}
                   for k, v in model.attributes.items() if v.displayable}

noalias_dumper = yaml.dumper.SafeDumper
noalias_dumper.ignore_aliases = lambda self, data: True
print(yaml.dump(yaml_definition, default_flow_style=False, Dumper=noalias_dumper))
