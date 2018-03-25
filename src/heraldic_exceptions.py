#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exceptions used in Heraldic program.
"""

from src.misc.logging import logger


class HeraldicException(Exception):
    pass


class DomainNotSupportedException(HeraldicException, ValueError):
    def __init__(self, domain):
        logger.log('WARN_DOMAIN_NOT_SUPPORTED', domain)


class DocumentNotFoundException(HeraldicException):
    pass


class DocumentExistsException(HeraldicException):
    def __init__(self, url):
        logger.log('INFO_DOC_ALREADY_UPTODATE', url)


class ParsingFailureException(HeraldicException):
    def __init__(self, message: str='Erreur de parsing'):
        self.message = message


class HTMLParsingFailureException(ParsingFailureException):
    def __init__(self, message: str='HTML parsing error'):
        self.message = message


class DateFormatFailureException(ParsingFailureException):
    def __init__(self, message='Date format error'):
        self.message = message


class DocumentNotChangedException(HeraldicException):
    def __init__(self, doc_id, url):
        logger.log('INFO_DOC_NOT_CHANGED', doc_id, url)
