#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from src.models.document_model import DocumentModel
from datetime import datetime


class DocumentRenderer(object):
    DATE_FORMAT = "%d/%m/%Y à %H:%M"

    def __init__(self, dm: DocumentModel) -> None:
        """
        Class initializer.

        :param dm: Document model which will contain all extracted items.
        """
        self.dm = dm

    def render_attribute(self, attribute) -> str:
        obj_attr = getattr(self.dm, attribute)
        if isinstance(obj_attr, list):
            return "\n".join(obj_attr)
        elif isinstance(obj_attr, datetime):
            return obj_attr.strftime(self.DATE_FORMAT)
        else:
            return obj_attr

    def update_attribute(self, attribute_name: str, value: str):
        obj_attr = getattr(self.dm, attribute_name)
        if isinstance(obj_attr, list):
            attribute_value = value.split("\n")
        elif isinstance(obj_attr, datetime):
            attribute_value = datetime.strptime(value, self.DATE_FORMAT)
        else:
            attribute_value = value
        setattr(self.dm, attribute_name, value)
