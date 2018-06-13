#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file can be used as a script to validate parsing of an article.
"""

from heraldic.models.document import Document
import sys
import heraldic.misc.exceptions as ex


def main(argv):
    url = input()
    d = Document(url, debug=True)
    try:
        d.gather(update=True)
    except ex.DocumentNotChangedException:
        pass
    for k, v in d.model.attributes.items():
        if v.extractible:
            if v.parsing_error:
                print(k + ' - ' + v.parsing_error)
            else:
                print(k + ' : ' + v.render_for_display())
            if v.suggestions:
                print(k + ' : suggestions : ' + ",".join(v.render_suggestions_for_display()))


if __name__ == "__main__":
    main(sys.argv[1:])
