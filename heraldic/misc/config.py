#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which implements Heraldic config.
"""

import configparser

DEFAULT_CONFIG_FILE = 'default.ini'
CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_FILE)
config.read(CONFIG_FILE)
