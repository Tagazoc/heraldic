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
quotes = ['«s’est rapidement dégradé»',
          '«Les médecins ne se prononcent pas à ce stade sur les suites pour son état de santé» et «il est aujourd’hui en soins intensifs et reste sous surveillance»',
          '«condamné»',
          '«actes de violence»',
          '«Si les circonstances restent encore à éclaircir, il semble établi que notre camarade a reçu des coups, '
          'notamment de casque de scooter, d’une violence telle que les pompiers ont été contraints de le transporter en urgence '
          'à l’hôpital où il a dû subir une opération chirurgicale. Le Parti socialiste condamne avec la plus grande '
          'fermeté cette agression»',
          '«La République en marche condamne les actes de violence commis à l’encontre de Boris Faure (...) Si les '
          'circonstances de cette altercation doivent encore être précisées, aucun comportement ne saurait justifier '
          'des actes de violence», «insultes racistes»', '«insultes racistes»',
          '«Je m’excuse pour la violence du geste. Et d’ailleurs, je condamne toute forme de violence car en dépit '
          'des paroles et insultes proférées, la violence n’est jamais la réaction appropriée (...) Je regrette '\
          'd’avoir cédé à la provocation»',
          '«assén(é) un coup de casque très violent puis un deuxième»',
          '«par terre, en sang»',
          '«Certains se croient autorisés à attribuer à Boris Faure (...) lors de l’altercation des visées ou des propos racistes. Pour ceux qui le connaissent, ces allégations (...) sont risibles et insultantes»', '«suites judiciaires appropriées en diffamation»', '«Les deux hommes entretiennent un violent contentieux politique depuis que le député a quitté le PS pour rejoindre les rangs macronistes, fin 2016»',
          '«opportunisme»']

href_sources = ['https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs']

explicit_sources = ['AFP']
