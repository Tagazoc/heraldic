#!/usr/b*in/env python
# -*- coding: utf-8 -*-
"""
Class used for document attributes.
"""

from datetime import datetime


class Attribute(object):
    DEFAULT_STORE_TYPE = 'text'
    DEFAULT_STORE_FORMAT = ''
    DEFAULT_VALUE = ""

    def __init__(self, **kwargs) -> None:
        self.desc = kwargs['desc'] if 'desc' in kwargs else ""
        """ Description of the attribute. """

        self.value = kwargs['value'] if 'value' in kwargs else self.DEFAULT_VALUE
        """ Default value """

        self.displayable = kwargs['displayable'] if 'displayable' in kwargs else True
        """ Whether it may be displayed or not. """

        self.revisable = kwargs['revisable'] if 'revisable' in kwargs else True
        """ Whether it may be manually updated. """

        self.extractible = kwargs['extractible'] if 'extractible' in kwargs else True
        """ Whether it can be automatically extracted with parsing. """

        self.storable = kwargs['storable'] if 'storable' in kwargs else self.DEFAULT_STORE_TYPE
        """ Whether it will be stored. """

        self.parse_error = None
        """ The parsing exception its extraction may have raised goes there. """

        self.store_format = self.DEFAULT_STORE_FORMAT
        """ Store format """

        self.initialized = kwargs['initialized'] if 'initialized' in kwargs else False
        """ Whether it is initialized or not (empty value does not suffice). """

        self.version_no = 0
        """ The version number when using different revisions of its document. """

    def __str__(self) -> str:
        return str(self.value)

    def render_for_display(self) -> str:
        return str(self.value)

    def render_for_store(self):
        return self.value

    def set_from_display(self, value: str) -> None:
        self.update(value)

    def set_from_store(self, value: str) -> None:
        self.update(value)

    def update(self, value):
        self.value = value

    def __setattr__(self, key, value):
        """ Catch value update to enable initialized flag """
        if key == "value":
            self.initialized = True
        super(Attribute, self).__setattr__(key, value)


class IntegerAttribute(Attribute):
    DEFAULT_STORE_TYPE = 'short'
    DEFAULT_VALUE = 0

    def __init__(self, **kwargs):
        super(IntegerAttribute, self).__init__(**kwargs)

    def set_from_display(self, value: str):
        self.update(int(value))


class StringAttribute(Attribute):
    def __init__(self, **kwargs):
        super(StringAttribute, self).__init__(**kwargs)


class StringListAttribute(Attribute):
    DEFAULT_VALUE = []

    def __init__(self, **kwargs):
        super(StringListAttribute, self).__init__(**kwargs)

    def render_for_display(self):
        return "\n".join(self.value)

    def set_from_display(self, value: str):
        splitted_values = value.splitlines() if value else []
        self.update(splitted_values)


class DateAttribute(Attribute):
    DATE_FORMAT = "%d/%m/%Y à %H:%M"
    DEFAULT_STORE_TYPE = 'date'
    DEFAULT_STORE_FORMAT = 'epoch_millis'
    DEFAULT_VALUE = datetime.fromtimestamp(0)

    def __init__(self, **kwargs):
        super(DateAttribute, self).__init__(**kwargs)

    def render_for_display(self):
        return self.value.strftime(self.DATE_FORMAT)

    def render_for_store(self):
        return round(self.value.timestamp())

    def set_from_display(self, value: str):
        self.update(datetime.strptime(value, self.DATE_FORMAT))

    def set_from_store(self, value: float):
        self.update(datetime.fromtimestamp(value))


class BooleanAttribute(Attribute):
    DEFAULT_VALUE = False

    def __init__(self, **kwargs):
        super(BooleanAttribute, self).__init__(**kwargs)

    def render_for_display(self):
        return "yes" if self.value else "no"

    def set_from_display(self, value: str):
        boolean = True if value == 'yes' else False
        self.update(boolean)

    def set_from_store(self, value: bool):
        self.update(value)
