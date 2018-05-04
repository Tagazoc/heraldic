#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exceptions used in Heraldic program.
"""

from src.misc.logging import logger


class HeraldicException(Exception):
    pass


class GatherException(HeraldicException):
    pass


class GatherError(GatherException):
    pass


class InvalidUrlException(GatherError):
    def __init__(self, url):
        logger.log('WARN_URL_INVALID', url)


class DomainNotSupportedException(GatherException):
    def __init__(self, domain):
        logger.log('WARN_DOMAIN_NOT_SUPPORTED', domain)


class DocumentNotFoundException(HeraldicException):
    pass


class DocumentExistsException(GatherException):
    def __init__(self, url):
        logger.log('INFO_DOC_ALREADY_UPTODATE', url)


class DocumentNotChangedException(DocumentExistsException):
    def __init__(self, doc_id, url):
        logger.log('INFO_DOC_NOT_CHANGED', doc_id, url)


class ParsingException(HeraldicException):
    BASE_MESSAGE = 'Generic parsing exception'
    LOGGING_TEMPLATE = ''

    def __init__(self):
        err_message = ",".join(self.__cause__.args) if self.__cause__ is not None else ''
        self.message = self.BASE_MESSAGE + ': ' + err_message


class MandatoryParsingException(ParsingException, GatherError):
    LOGGING_TEMPLATE = 'WARN_MANDATORY_PARSING_ERROR'


class OptionalParsingException(ParsingException):
    LOGGING_TEMPLATE = 'WARN_ATTRIBUTE_PARSING_ERROR'


class HTMLParsingException(OptionalParsingException):
    BASE_MESSAGE = 'HTML parsing error'


class DateFormatParsingException(OptionalParsingException):
    BASE_MESSAGE = 'Date format error'
