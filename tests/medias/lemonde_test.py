#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test lib for media "Le Monde", which should only be imported from "media_gathering_test.py" file.
"""

url = 'http://www.lemonde.fr/politique/article/2017/09/08/parlement-europeen-un-haut-responsable-du-groupe-fn' \
          '-ecarte_5182958_823448.html?xtmc=mediapart&xtcr=3'

response_beginning = """<!doctype html>
<!--[if lt IE 9]><html class="ie"><![endif]-->
<!--[if IE 9]><html class="ie9"><![endif]-->
<!--[if gte IE 9]><!-->
<html lang="fr">
<!--<![endif]-->

<head>
<!-- Google Tag Manager -->"""

title = 'Parlement européen\xa0: un haut responsable du groupe FN écarté'

description = '«\xa0Le divorce était devenu inéluctable\xa0», a déclaré le secrétaire général du groupe d’extrême ' \
              'droite Europe des Nations et des libertés au Parlement européen.'

category = 'politique'

doc_publication_time_str = '08/09/2017 15:34'
doc_update_time_str = '08/09/2017 21:01'

href_sources = [
    'https://www.mediapart.fr/journal/france/080917/fn-sophie-montel-iconoclaste-mise-au-ban',
    '//twitter.com/olivierfaye/status/906057841563369472',
    'https://www.google.fr/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved'
    '=0ahUKEwjixPDY0pXWAhVLbBoKHUfvADMQFggmMAA&url=http%3A%2F%2Fwww.lemonde.fr%2Fles-decodeurs%2Farticle'
    '%2F2017%2F02%2F02%2Fles-trois-affaires-qui-menacent-marine-le-pen-et-le-front'
    '-national_5073473_4355770.html&usg=AFQjCNFxmn4-b-L9PlO9TJRJnqT2rJKgvg']

explicit_sources = ['AFP']
