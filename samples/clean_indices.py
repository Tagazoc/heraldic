#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete all indices, then recreate them.
"""

import sys
from heraldic.store.elastic import DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex
from typing import Optional


def query_yes_no(question, default: Optional[str]="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if query_yes_no("You will lose all documents stored in elasticsearch. Continue?", None):
    #DocumentIndex.delete()
    #OldVersionIndex.delete()
    ErrorIndex.delete()
    #SuggestionIndex.delete()
    #FeedsIndex.delete()

    #DocumentIndex.create()
    #OldVersionIndex.create()
    ErrorIndex.create()
    #SuggestionIndex.create()
    #FeedsIndex.create()
