#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exceptions used in Heraldic program.
"""

from heraldic.misc.logging import logger


class HeraldicException(Exception):
    pass


class IndexerConnectionError(HeraldicException, ConnectionError):
    pass


class DeletionError(HeraldicException):
    pass


class GatherException(HeraldicException):
    pass


class GatherError(GatherException):
    pass


class InvalidUrlException(GatherError):
    def __init__(self, url, do_not_log=False):
        super(InvalidUrlException, self).__init__()
        if not do_not_log:
            logger.log('WARN_URL_INVALID', url)


class DomainNotSupportedException(GatherException):
    def __init__(self, domain, do_not_log=False):
        self.domain = domain
        if not do_not_log:
            logger.log('WARN_DOMAIN_NOT_SUPPORTED', domain)


class UrlNotSupportedException(GatherException):
    def __init__(self, url, final_url, do_not_log=False):
        if not do_not_log:
            logger.log('WARN_URL_NOT_ARTICLE', url, final_url)


class DocumentNotArticleException(GatherException):
    def __init__(self, url, final_url, do_not_log=False):
        if not do_not_log:
            logger.log('WARN_CONTENT_NOT_SUPPORTED', url, final_url)


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

    def __init__(self, attribute, url, err):
        super(ParsingException, self).__init__()
        self.attribute = attribute
        err_message = ",".join(err.args) if err is not None else ''
        self.message = self.BASE_MESSAGE + ': ' + err_message
        logger.log(self.LOGGING_TEMPLATE, attribute, url, self.message)


class MandatoryParsingException(ParsingException, GatherError):
    LOGGING_TEMPLATE = 'WARN_MANDATORY_PARSING_ERROR'


class OptionalParsingException(ParsingException, GatherError):
    LOGGING_TEMPLATE = 'WARN_ATTRIBUTE_PARSING_ERROR'


class HTMLParsingException(OptionalParsingException):
    BASE_MESSAGE = 'HTML parsing error'


class DateFormatParsingException(OptionalParsingException):
    BASE_MESSAGE = 'Date format error'


class FeedUnavailable(HeraldicException):
    def __init__(self, url, status):
        logger.log('WARN_FEED_UNAVAILABLE', url, status)
