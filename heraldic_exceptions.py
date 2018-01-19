#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exceptions used in Heraldic program.
"""


class HeraldicException(Exception):
    pass


class DomainNotSupportedException(HeraldicException, ValueError):
    pass


class DocumentNotFoundException(HeraldicException):
    pass


class ParsingFailureException(HeraldicException):
    pass


class HTMLParsingFailureException(ParsingFailureException):
    def __init__(self, parse_string: str=''):
        self.parse_string = parse_string


class DateFormatFailureException(ParsingFailureException):
    def __init__(self, msg=''):
        self.msg = msg

