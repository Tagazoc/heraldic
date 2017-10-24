#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test lib for media "Libération", which should only be imported from "media_gathering_test.py" file.
"""

url = 'http://www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute' \
      '-lrem_1593251'

response_beginning = '''<!DOCTYPE html>












<html lang="fr">'''

title = "Un cadre du PS en «soins intensifs» après une agression par un député LREM - Libération"
description = "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins " \
              "intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. "
category = "Politique"

doc_publication_time_str = '31/08/2017 13:03'
doc_update_time_str = '31/08/2017 14:20'

href_sources = ['https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs']

explicit_sources = ['AFP']
