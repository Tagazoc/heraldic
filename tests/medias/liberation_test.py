#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test lib for media "Libération", which should only be imported from "media_gathering_test.py" file.
"""

media_id = 'liberation'
media_name = 'Libération'
article_filepath_update = 'tests/medias/article_liberation_update.htm'
article_filepath_error = 'tests/medias/article_liberation_error.htm'
article_filepath_error_solved = 'tests/medias/article_liberation_error_solved.htm'

url = "http://www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251"
bad_domain_url = "http://www.laberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251"

doc_dict = {
    'category': 'Politique',
    'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est"
                   " en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    'doc_publication_time': '2017-08-31T13:03:36Z',
    'doc_update_time': '2017-08-31T14:20:10Z',
    'document_type': 'article',
    'href_sources': [
        'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
    'keywords': ['actualités', 'news', 'Agence France-Presse', 'Paris', 'Pompier', 'Mediapart', 'Blog', 'Assen',
                 'Jabber', 'Primaire présidentielle socialiste de 2011', 'Surréalisme', 'Scooter', 'Violence',
                 'Urgences', 'Réanimation', 'Arabes', 'En marche !', 'Rue Broca', 'Député', 'Racisme', 'Marianne',
                 'Libération', 'Hebdomadaire', 'Diffamation', 'Didier Le Bret', 'PS', 'Assemblée nationale',
                 'Famille', 'Hôpital', 'Socialiste', 'Élections législatives de 2012', "Mohamed M'jid"],
    'media': 'liberation',
    'news_agency': 'AFP',
    'subscribers_only': False,
    'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
    'urls': [
        'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
    'version_no': 1,
    'words': []
}
suggestion_dict = {
}

update_doc_dict = {
    'category': 'Politique',
    'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    'doc_publication_time': '2017-08-31T13:03:36Z',
    'doc_update_time': '2017-08-31T14:21:10Z',
    'document_type': 'article',
    'href_sources': [
        'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
    'keywords': ['Violence', 'Socialiste', 'Agence France-Presse', 'Jabber', 'Surréalisme', 'Paris', 'Hebdomadaire',
                 'Assemblée nationale', 'Mediapart', 'Arabes', 'Diffamation', "Mohamed M'jid", 'Famille', 'Marianne',
                 'Député', 'En marche !', 'Urgences', 'Didier Le Bret', 'Assen', 'Blog', 'actualités', 'PS',
                 'Élections législatives de 2012', 'Hôpital', 'Scooter', 'Rue Broca', 'news', 'Réanimation', 'Racisme',
                 'Primaire présidentielle socialiste de 2011', 'Pompier', 'Libération'],
    'media': 'liberation',
    'news_agency': 'AFP',
    'subscribers_only': False,
    'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
    'urls': [
        'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
    'version_no': 2,
    'words': []
}

update_doc_versions = [
    {
        'category': 'Politique',
        'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
        'doc_publication_time': '2017-08-31T13:03:36Z',
        'doc_update_time': '2017-08-31T14:20:10Z',
        'document_type': 'article',
        'href_sources': [
            'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
        'keywords': ['Hôpital', 'Rue Broca', 'actualités', 'Assen', 'Réanimation', 'Paris', 'news', 'Didier Le Bret',
                     'Famille', 'Hebdomadaire', 'Surréalisme', 'Pompier', 'Scooter', 'Marianne', 'En marche !', 'Blog',
                     'Arabes', 'Député', 'Socialiste', 'Diffamation', 'Élections législatives de 2012', "Mohamed M'jid",
                     'Libération', 'PS', 'Racisme', 'Mediapart', 'Assemblée nationale', 'Jabber', 'Violence',
                     'Urgences', 'Primaire présidentielle socialiste de 2011', 'Agence France-Presse'],
        'media': 'liberation',
        'news_agency': 'AFP',
        'subscribers_only': False,
        'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
        'urls': [
            'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
        'version_no': 1
    },
    {
        'doc_update_time': '2017-08-31T14:21:10Z',
        'keywords': ['Jabber', 'PS', 'Hebdomadaire', 'Assemblée nationale', 'Élections législatives de 2012',
                     'Didier Le Bret', 'Libération', 'Surréalisme', 'Réanimation', 'Hôpital', 'Assen', 'Paris',
                     'Pompier', 'En marche !', 'Rue Broca', 'actualités', 'Urgences',
                     'Primaire présidentielle socialiste de 2011', 'Marianne', 'Socialiste', 'news', 'Diffamation',
                     'Mediapart', 'Violence', 'Racisme', 'Blog', "Mohamed M'jid", 'Scooter', 'Famille', 'Arabes',
                     'Député', 'Agence France-Presse'],
        'version_no': 2
    }
]

error_doc_dict = {
    'category': 'Politique',
    'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    'doc_publication_time': '2017-08-31T13:03:36Z',
    'doc_update_time': '2017-08-31T14:21:10Z',
    'document_type': 'article',
    'href_sources': [
        'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
    'keywords': ['Violence', 'Socialiste', 'Agence France-Presse', 'Jabber', 'Surréalisme', 'Paris', 'Hebdomadaire',
                 'Assemblée nationale', 'Mediapart', 'Arabes', 'Diffamation', "Mohamed M'jid", 'Famille', 'Marianne',
                 'Député', 'En marche !', 'Urgences', 'Didier Le Bret', 'Assen', 'Blog', 'actualités', 'PS',
                 'Élections législatives de 2012', 'Hôpital', 'Scooter', 'Rue Broca', 'news', 'Réanimation', 'Racisme',
                 'Primaire présidentielle socialiste de 2011', 'Pompier', 'Libération'],
    'media': 'liberation',
    'news_agency': 'Reuters',
    'subscribers_only': False,
    'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
    'urls': [
        'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
    'version_no': 3,
    'words': []
}

error_doc_versions = [
    {
        'category': 'Politique',
        'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
        'doc_publication_time': '2017-08-31T13:03:36Z',
        'doc_update_time': '2017-08-31T14:20:10Z',
        'document_type': 'article',
        'href_sources': [
            'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
        'keywords': ['Hôpital', 'Rue Broca', 'actualités', 'Assen', 'Réanimation', 'Paris', 'news', 'Didier Le Bret',
                     'Famille', 'Hebdomadaire', 'Surréalisme', 'Pompier', 'Scooter', 'Marianne', 'En marche !', 'Blog',
                     'Arabes', 'Député', 'Socialiste', 'Diffamation', 'Élections législatives de 2012', "Mohamed M'jid",
                     'Libération', 'PS', 'Racisme', 'Mediapart', 'Assemblée nationale', 'Jabber', 'Violence',
                     'Urgences', 'Primaire présidentielle socialiste de 2011', 'Agence France-Presse'],
        'media': 'liberation',
        'news_agency': 'AFP',
        'subscribers_only': False,
        'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
        'urls': [
            'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
        'version_no': 1
    },
    {
        'doc_update_time': '2017-08-31T14:21:10Z',
        'keywords': ['Jabber', 'PS', 'Hebdomadaire', 'Assemblée nationale', 'Élections législatives de 2012',
                     'Didier Le Bret', 'Libération', 'Surréalisme', 'Réanimation', 'Hôpital', 'Assen', 'Paris',
                     'Pompier', 'En marche !', 'Rue Broca', 'actualités', 'Urgences',
                     'Primaire présidentielle socialiste de 2011', 'Marianne', 'Socialiste', 'news', 'Diffamation',
                     'Mediapart', 'Violence', 'Racisme', 'Blog', "Mohamed M'jid", 'Scooter', 'Famille', 'Arabes',
                     'Député', 'Agence France-Presse'],
        'version_no': 2
    },
    {
        'news_agency': 'Reuters',
        'version_no': 3
    }
]

error_doc_errors = {
    'title': "Generic parsing exception: 'NoneType' object has no attribute 'get'"
}

error_solved_doc_dict = {
    'category': 'Politique',
    'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    'doc_publication_time': '2017-08-31T13:03:36Z',
    'doc_update_time': '2017-08-31T14:21:10Z',
    'document_type': 'article',
    'href_sources': [
        'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
    'keywords': ['Famille', 'Marianne', 'En marche !', 'Diffamation', 'Assemblée nationale', 'Didier Le Bret', 'Blog',
                 'Hebdomadaire', 'Élections législatives de 2012', 'actualités',
                 'Primaire présidentielle socialiste de 2011', 'news', 'Député', 'Libération', 'Arabes', 'Socialiste',
                 'Urgences', 'Jabber', 'Assen', 'Hôpital', 'PS', 'Surréalisme', 'Réanimation', 'Paris',
                 'Agence France-Presse', 'Pompier', 'Violence', "Mohamed M'jid", 'Mediapart', 'Scooter', 'Rue Broca',
                 'Racisme'],
    'media': 'liberation',
    'news_agency': 'Reuters',
    'subscribers_only': False,
    'title': 'Un cadre du PS en «soins très intensifs» après une agression par un député LREM',
    'urls': [
        'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
    'version_no': 4,
    'words': []
}

error_solved_doc_versions = [
    {
        'category': 'Politique',
        'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
        'doc_publication_time': '2017-08-31T13:03:36Z',
        'doc_update_time': '2017-08-31T14:20:10Z',
        'document_type': 'article',
        'href_sources': [
            'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
        'keywords': ['Urgences', 'Assen', 'Libération', 'Scooter', 'Rue Broca',
                     'Didier Le Bret', 'Arabes', 'En marche !', 'actualités', 'Mediapart',
                     'Hôpital', 'Paris', 'Jabber', 'Hebdomadaire', 'Diffamation', 'Blog',
                     "Mohamed M'jid", 'Violence', 'Primaire présidentielle socialiste de 2011',
                     'Agence France-Presse', 'Député', 'Marianne', 'Réanimation', 'Famille',
                     'PS', 'Assemblée nationale', 'Surréalisme', 'Pompier', 'news', 'Racisme',
                     'Socialiste', 'Élections législatives de 2012'],
        'media': 'liberation',
        'news_agency': 'AFP',
        'subscribers_only': False,
        'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
        'urls': [
            'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
        'version_no': 1
    },
    {
        'doc_update_time': '2017-08-31T14:21:10Z',
        'keywords': ['Famille', 'Marianne', 'En marche !', 'Diffamation',
                     'Assemblée nationale', 'Didier Le Bret', 'Blog', 'Hebdomadaire',
                     'Élections législatives de 2012', 'actualités',
                     'Primaire présidentielle socialiste de 2011', 'news', 'Député',
                     'Libération', 'Arabes', 'Socialiste', 'Urgences', 'Jabber', 'Assen',
                     'Hôpital', 'PS', 'Surréalisme', 'Réanimation', 'Paris',
                     'Agence France-Presse', 'Pompier', 'Violence', "Mohamed M'jid",
                     'Mediapart', 'Scooter', 'Rue Broca', 'Racisme'],
        'version_no': 2
    },
    {
        'news_agency': 'Reuters',
        'version_no': 3
    },
    {
        'title': 'Un cadre du PS en «soins très intensifs» après une agression par un député LREM',
        'version_no': 4
    }
]

update_inplace_doc_dict = {
    'category': 'Politique',
    'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
    'doc_publication_time': '2017-08-31T13:03:36Z',
    'doc_update_time': '2017-08-31T14:20:10Z',
    'document_type': 'article',
    'href_sources': [
        'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
    'keywords': ['Famille', 'Marianne', 'En marche !', 'Diffamation', 'Assemblée nationale', 'Didier Le Bret', 'Blog',
                 'Hebdomadaire', 'Élections législatives de 2012', 'actualités',
                 'Primaire présidentielle socialiste de 2011', 'news', 'Député', 'Libération', 'Arabes', 'Socialiste',
                 'Urgences', 'Jabber', 'Assen', 'Hôpital', 'PS', 'Surréalisme', 'Réanimation', 'Paris',
                 'Agence France-Presse', 'Pompier', 'Violence', "Mohamed M'jid", 'Mediapart', 'Scooter', 'Rue Broca',
                 'Racisme'],
    'media': 'liberation',
    'news_agency': 'AFP',
    'subscribers_only': False,
    'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
    'urls': [
        'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
    'version_no': 4,
    'words': []
}

update_inplace_doc_versions = [
    {
        'category': 'Politique',
        'description': "Le premier secrétaire de la fédération PS des Français de l'étranger, Boris Faure, est en «soins intensifs» après l’agression commise mercredi par un député REM, M’jid El Guerrab. ",
        'doc_publication_time': '2017-08-31T13:03:36Z',
        'doc_update_time': '2017-08-31T14:20:10Z',
        'document_type': 'article',
        'href_sources': [
            'www.marianne.net/politique/le-responsable-ps-agresse-par-un-depute-lrem-est-en-soins-intensifs'],
        'keywords': ['Urgences', 'Assen', 'Libération', 'Scooter', 'Rue Broca',
                     'Didier Le Bret', 'Arabes', 'En marche !', 'actualités', 'Mediapart',
                     'Hôpital', 'Paris', 'Jabber', 'Hebdomadaire', 'Diffamation', 'Blog',
                     "Mohamed M'jid", 'Violence', 'Primaire présidentielle socialiste de 2011',
                     'Agence France-Presse', 'Député', 'Marianne', 'Réanimation', 'Famille',
                     'PS', 'Assemblée nationale', 'Surréalisme', 'Pompier', 'news', 'Racisme',
                     'Socialiste', 'Élections législatives de 2012'],
        'media': 'liberation',
        'news_agency': 'AFP',
        'subscribers_only': False,
        'title': 'Un cadre du PS en «soins intensifs» après une agression par un député LREM',
        'urls': [
            'www.liberation.fr/france/2017/08/31/un-cadre-du-ps-en-soins-intensifs-apres-une-agression-par-un-depute-lrem_1593251'],
        'version_no': 1
    },
    {
        'keywords': ['Famille', 'Marianne', 'En marche !', 'Diffamation',
                     'Assemblée nationale', 'Didier Le Bret', 'Blog', 'Hebdomadaire',
                     'Élections législatives de 2012', 'actualités',
                     'Primaire présidentielle socialiste de 2011', 'news', 'Député',
                     'Libération', 'Arabes', 'Socialiste', 'Urgences', 'Jabber', 'Assen',
                     'Hôpital', 'PS', 'Surréalisme', 'Réanimation', 'Paris',
                     'Agence France-Presse', 'Pompier', 'Violence', "Mohamed M'jid",
                     'Mediapart', 'Scooter', 'Rue Broca', 'Racisme'],
        'version_no': 2
    },
    {
        'version_no': 3
    },
    {
        'version_no': 4
    }
]
