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


class DocumentExistsException(HeraldicException):
    pass


class ParsingFailureException(HeraldicException):
    def __init__(self, message: str='Erreur de parsing'):
        self.message = message


class HTMLParsingFailureException(ParsingFailureException):
    def __init__(self, message: str='Erreur de parsing HTML'):
        self.message = message


class DateFormatFailureException(ParsingFailureException):
    def __init__(self, message=''):
        self.message = message


class DocumentNotChangedException(HeraldicException):
    pass
