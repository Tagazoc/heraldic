#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test lib for media "Libération", which should only be imported from "media_gathering_test.py" file.
"""

url = "http://www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251"

doc_dict = {
    "media": "liberation",
    "version_no": "1",
    "urls": "www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251",
    "category": "Politique",
    "title": "Un cadre du PS en «soins intensifs» après une agression par un député LREM",
    "description": "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    "doc_publication_time": "31/08/2017 à 13:03",
    "doc_update_time": "31/08/2017 à 14:20",
    "href_sources": "https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs",
    "news_agency": "AFP",
    "quoted_entities": "",
    "contains_private_sources": ""
}

suggestion_dict = {
}

update_doc_dict = {
    "explicit_sources": "Agence France Presse\nToto",
    "contains_private_sources": "yes",
    "quoted_entities": "François Fillon\nJean-Marc Morandini"
}

update_result_dict = {
    "media": "liberation",
    "version_no": "2",
    "urls": "www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251",
    "category": "Politique",
    "title": "Un cadre du PS en «soins intensifs» après une agression par un député LREM",
    "description": "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    "doc_publication_time": "31/08/2017 à 13:03",
    "doc_update_time": "31/08/2017 à 14:20",
    "href_sources": "https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs",
    "explicit_sources": "Agence France Presse\nToto",
    "news_agency": "AFP",
    "contains_private_sources": "yes",
    "quoted_entities": "François Fillon\nJean-Marc Morandini"
}

update_old_model_list = [
    {
        "version_no": "1",
        "explicit_sources": "",
        "quoted_entities": "",
        "contains_private_sources": "no"
    }
]

error_result_dict = {
    "media": "liberation",
    "version_no": "3",
    "urls": "www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251",
    "category": "Politique",
    "title": "Un cadre du PS en «soins intensifs» après une agression par un député LREM",
    "description": "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    "doc_publication_time": "31/08/2017 à 13:03",
    "doc_update_time": "31/08/2017 à 14:21",
    "href_sources": "https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs",
    "explicit_sources": "Agence France Presse\nToto",
    "news_agency": "",
    "contains_private_sources": "yes",
    "quoted_entities": "François Fillon\nJean-Marc Morandini"
}

errors_list = [
    "title"
]

error_old_model_list = [
    {
        "version_no": "1",
        "explicit_sources": "",
        "quoted_entities": "",
        "contains_private_sources": "no"
    },
    {
        "version_no": "2",
        "doc_update_time": "31/08/2017 à 14:20"
    }
]

final_gather_dict = {
    "media": "liberation",
    "version_no": "4",
    "urls": "www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251",
    "category": "Politique",
    "title": "Un cadre du PS en «soins intensifs» après une agression par un député LREM",
    "description": "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    "doc_publication_time": "31/08/2017 à 13:03",
    "doc_update_time": "31/08/2017 à 14:20",
    "href_sources": "https://www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs",
    "explicit_sources": "Agence France Presse\nToto",
    "news_agency": "AFP",
    "contains_private_sources": "yes",
    "quoted_entities": "François Fillon\nJean-Marc Morandini"
}

final_old_model_list = [
    {
        "version_no": "1",
        "explicit_sources": "",
        "quoted_entities": "",
        "contains_private_sources": "no"
    },
    {
        "version_no": "2",
        "doc_update_time": "31/08/2017 à 14:20"
    },
    {
        "version_no": "3",
        "doc_update_time": "31/08/2017 à 14:21"
    }
]
