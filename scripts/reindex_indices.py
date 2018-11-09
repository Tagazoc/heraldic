#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Delete all indices, then recreate them.
"""

import os
import sys
import tempfile
import subprocess
from heraldic.store.elastic import DocumentIndex, OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex


reindex_conf_template = """
actions:
  1:
    description: "Reindex %s into %s"
    action: reindex
    options:
      disable_action: False
      wait_interval: 9
      max_wait: -1
      request_body:
        source:
          index: %s
        dest:
          index: %s
    filters:
    - filtertype: none
"""
alias_conf_template = """
actions:
  1:
    action: alias
    description: >-
      Alias indice %s into %s
    options:
      name: %s
      warn_if_no_indices: False
      disable_action: False
    add:
      filters:
      - filtertype: pattern
        kind: regex
        value: ^%s$
"""

delete_indices_conf_template = """
actions:
  1:
    action: delete_indices
    description: >-
      Delete indice %s.
    options:
      disable_action: False
    filters:
    - filtertype: pattern
      kind: regex
      value: ^%s$
"""

curator_cmd = "curator %s"


def main(argv):
    for index in [OldVersionIndex, ErrorIndex, SuggestionIndex, FeedsIndex]:
        old_name = index.INDEX_NAME
        new_name = old_name + argv[0]
        index.INDEX_NAME = new_name
        index.create()
        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write(reindex_conf_template % (old_name, new_name, old_name, new_name))
        file_name = f.name
        f.close()

        result = subprocess.run((curator_cmd % file_name).split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
        os.remove(file_name)
        if result.returncode != 0:
            exit(1)

        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write(delete_indices_conf_template % (old_name, old_name))
        file_name = f.name
        f.close()
        result = subprocess.run((curator_cmd % file_name).split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
        os.remove(file_name)
        if result.returncode != 0:
            exit(2)

        f = tempfile.NamedTemporaryFile('w', delete=False)
        f.write(alias_conf_template % (new_name, old_name, old_name, new_name))
        file_name = f.name
        f.close()
        result = subprocess.run((curator_cmd % file_name).split(" "), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
        os.remove(file_name)


if __name__ == "__main__":
    main(sys.argv[1:])

