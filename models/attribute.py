#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used for document attributes.
"""

from datetime import datetime


class Attribute(object):
    def __init__(self, **kwargs) -> None:
        self.desc = kwargs['desc'] if 'desc' in kwargs else ""
        self.value = None
        self.displayable = kwargs['displayable'] if 'displayable' in kwargs else True
        self.revisable = kwargs['revisable'] if 'revisable' in kwargs else True
        self.extractible = kwargs['extractible'] if 'extractible' in kwargs else True

    def __str__(self) -> str:
        return str(self.value)

    def render(self) -> str:
        return str(self.value)

    def update(self, value: str) -> None:
        self.value = value


class IntegerAttribute(Attribute):
    def __init__(self, **kwargs):
        super(IntegerAttribute, self).__init__(**kwargs)
        self.value = 0

    def update(self, value: str):
        self.value = int(value)


class StringAttribute(Attribute):
    def __init__(self, **kwargs):
        super(StringAttribute, self).__init__(**kwargs)
        self.value = ""


class StringListAttribute(Attribute):
    def __init__(self, **kwargs):
        super(StringListAttribute, self).__init__(**kwargs)
        self.value = []

    def render(self):
        return "\n".join(self.value)

    def update(self, value: str):
        self.value = value.split("\n")


class DateAttribute(Attribute):
    DATE_FORMAT = "%d/%m/%Y à %H:%M"

    def __init__(self, **kwargs):
        super(DateAttribute, self).__init__(**kwargs)
        self.value = datetime.now()

    def render(self):
        return self.value.strftime(self.DATE_FORMAT)

    def update(self, value: str):
        self.value = datetime.strptime(value, self.DATE_FORMAT)


class BooleanAttribute(Attribute):
    def __init__(self, **kwargs):
        super(BooleanAttribute, self).__init__(**kwargs)
        self.value = False

    def render(self):
        return "Oui" if self.value else "Non"

    def update(self, value: str):
        self.value = True if value == 'yes' else False
