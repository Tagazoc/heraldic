#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exceptions used in Heraldic program.
"""


class HeraldicException(Exception):
    pass


class DomainNotSupportedException(HeraldicException, ValueError):
    pass
