#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used for document attributes.
"""

from datetime import datetime


class Attribute(object):
    DEFAULT_STORE_TYPE = 'text'
    DEFAULT_STORE_FORMAT = ''

    def __init__(self, **kwargs) -> None:
        self.desc = kwargs['desc'] if 'desc' in kwargs else ""
        self.value = None
        self.displayable = kwargs['displayable'] if 'displayable' in kwargs else True
        self.revisable = kwargs['revisable'] if 'revisable' in kwargs else True
        self.extractible = kwargs['extractible'] if 'extractible' in kwargs else True
        self.storable = kwargs['storable'] if 'storable' in kwargs else self.DEFAULT_STORE_TYPE
        self.store_format = self.DEFAULT_STORE_FORMAT

        self.old_value = None

    def __str__(self) -> str:
        return str(self.value)

    def render_for_display(self) -> str:
        return str(self.value)

    def render_for_store(self) -> str:
        return str(self.value)

    def update_from_display(self, value: str) -> None:
        self.update(value)

    def update_from_store(self, value: str) -> None:
        self.update(value)

    def update(self, value):
        self.old_value = self.value
        self.value = value


class IntegerAttribute(Attribute):
    def __init__(self, **kwargs):
        super(IntegerAttribute, self).__init__(**kwargs)
        self.value = 0

    def update_from_display(self, value: str):
        self.update(int(value))


class StringAttribute(Attribute):
    def __init__(self, **kwargs):
        super(StringAttribute, self).__init__(**kwargs)
        self.value = ""


class StringListAttribute(Attribute):
    def __init__(self, **kwargs):
        super(StringListAttribute, self).__init__(**kwargs)
        self.value = []

    def render_for_display(self):
        return "\n".join(self.value)

    def update_from_display(self, value: str):
        self.update(value.split("\n"))


class DateAttribute(Attribute):
    DATE_FORMAT = "%d/%m/%Y à %H:%M"
    DEFAULT_STORE_TYPE = 'date'
    DEFAULT_STORE_FORMAT = 'epoch_millis'

    def __init__(self, **kwargs):
        super(DateAttribute, self).__init__(**kwargs)
        self.value = datetime.now()

    def render_for_display(self):
        return self.value.strftime(self.DATE_FORMAT)

    def render_for_store(self):
        return round(self.value.timestamp())

    def update_from_display(self, value: str):
        self.update(datetime.strptime(value, self.DATE_FORMAT))

    def update_from_store(self, value: float):
        self.update(datetime.fromtimestamp(value))


class BooleanAttribute(Attribute):
    def __init__(self, **kwargs):
        super(BooleanAttribute, self).__init__(**kwargs)
        self.value = False

    def render_for_display(self):
        return "Oui" if self.value else "Non"

    def update_from_display(self, value: str):
        boolean = True if value == 'yes' else False
        self.update(boolean)

    def update_from_store(self, value: bool):
        self.update(value)
