#!/usr/b*in/env python
# -*- coding: utf-8 -*-
"""
Class used for document attributes.
"""

from datetime import datetime
from re import match
from typing import List, Optional


def uninitialized_display_wrapper(func):
    def wrapper(self):
        if not self.initialized:
            return ''
        else:
            return func(self)
    return wrapper


class Attribute(object):
    DEFAULT_STORE_TYPE = 'text'
    DEFAULT_STORE_FORMAT = ''
    DEFAULT_VALUE = ""
    DEFAULT_INVALIDATION_TEXT = "Valeur incorrecte."

    def __init__(self, **kwargs) -> None:
        self.desc: str = kwargs['desc'] if 'desc' in kwargs else ""
        """ Description of the attribute. """

        self.value = kwargs['value'] if 'value' in kwargs else self.DEFAULT_VALUE
        """ Default value """

        self.displayable: bool = kwargs['displayable'] if 'displayable' in kwargs else True
        """ Whether it may be displayed or not. """

        self.revisable: bool = kwargs['revisable'] if 'revisable' in kwargs else True
        """ Whether it may be manually updated. """

        self.extractible: bool = kwargs['extractible'] if 'extractible' in kwargs else True
        """ Whether it can be automatically extracted with parsing. """

        self.storable: str = kwargs['storable'] if 'storable' in kwargs else self.DEFAULT_STORE_TYPE
        """ Whether it will be stored. """

        self.initialized: bool = kwargs['initialized'] if 'initialized' in kwargs else False
        """ Whether it is initialized or not (empty value does not suffice). """

        self.store_format = self.DEFAULT_STORE_FORMAT
        """ Store format """

        self.parsing_error: Optional[str] = None
        """ Parsing error (if any) for this attribute. """

        self.version_no: int = 0
        """ The version number when using different revisions of its document. """

        self.suggestions: List[str] = []
        """ If it is both extractible and revisable, extractions will come as suggestions. """

    def __str__(self) -> str:
        return str(self.value)

    @uninitialized_display_wrapper
    def render_for_display(self) -> str:
        return str(self.value)

    def render_for_store(self):
        return self.value

    def render_suggestions_for_store(self) -> List[str]:
        return self.suggestions

    def render_suggestions_for_display(self) -> List[str]:
        return self.suggestions

    def set_from_extraction(self, value) -> None:
        if self.revisable and self.extractible:
            if isinstance(value, list):
                self.suggestions.extend(value)
            else:
                self.suggestions.append(value)
        else:
            self.update(value)

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

    def validate(self, field):
        return self.validate_value(field)

    def validate_value(self, field):
        return True

    @property
    def validate_failure_text(self):
        return self.DEFAULT_INVALIDATION_TEXT


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

    @uninitialized_display_wrapper
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
    DEFAULT_INVALIDATION_TEXT = 'Le format doit être le suivant : 18/07/2019 à 12:27'

    def __init__(self, **kwargs):
        super(DateAttribute, self).__init__(**kwargs)

    @uninitialized_display_wrapper
    def render_for_display(self):
        return self.value.strftime(self.DATE_FORMAT)

    def render_for_store(self):
        return round(self.value.timestamp())

    def set_from_display(self, value: str):
        self.update(datetime.strptime(value, self.DATE_FORMAT))

    def set_from_store(self, value: float):
        self.update(datetime.fromtimestamp(value))

    def validate_value(self, field):
        return True if match(r'\d{2}/\d{2}/\d{4} à \d{2}:\d{2}', field) else False


class BooleanAttribute(Attribute):
    DEFAULT_VALUE = False

    def __init__(self, **kwargs):
        super(BooleanAttribute, self).__init__(**kwargs)

    @uninitialized_display_wrapper
    def render_for_display(self):
        return "yes" if self.value else "no"

    def set_from_display(self, value: str):
        boolean = True if value == 'yes' else False
        self.update(boolean)

    def set_from_store(self, value: bool):
        self.update(value)
