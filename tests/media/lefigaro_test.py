#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test lib for media "Le Figaro", which should only be imported from "media_gathering_test.py" file.
"""

# http://www.lefigaro.fr/flash-actu/2016/12/23/97001-20161223FILWWW00292-attenta-de-nice-estrosi-decide-de-porter-plainte-suite-a-l-enquete-de-mediapart.php

url = 'http://www.lefigaro.fr/flash-actu/2016/12/23/97001-20161223FILWWW00292-attenta-de-nice-estrosi-decide-de' \
      '-porter-plainte-suite-a-l-enquete-de-mediapart.php'

response_beginning = """<!DOCTYPE html>
<html lang="fr" data-async-path="/"
      xmlns="http://www.w3.org/1999/xhtml"
      xmlns:og="http://opengraphprotocol.org/schema/"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:fp="http://plus.lefigaro.fr/fp/elements/1.0/" version="XHTML+RDFa 1.0">
    <head>
        <meta charset="UTF-8" />"""

title = "Attentat de Nice: Estrosi décide de porter plainte suite à l'enquête de Mediapart"

description = "Dans une interview accordée au site internet du journal Le Point, Christian Estrosi, président Les " \
              "Républicains de la Région PACA et premier adjoint.."

category = 'Flash Actu'

doc_publication_time_str = '23/12/2016 20:45'
doc_update_time_str = '23/12/2016 21:08'

href_sources = [
    'http://www.lepoint.fr/politique/attentat-de-nice-mediapart-accable-christian-estrosi-23-12-2016-2092619_20.php'
    '?campaign_id=A100',
    'https://www.mediapart.fr/journal/france/231216/attentat-de-nice-le-terroriste-pu-proceder'
                         '-onze-reperages?page_article=1'
]

explicit_sources = ['AFP']
