Fonctionnement général
======================

Le fonctionnement d'Heraldic est simple : les articles de divers sites Web sont récupérés via leur URL, via diverses méthodes (suivi de flux RSS, soumission manuelle, etc.). La page Web est alors analysée et divers contenus intéressants en sont extraits : titre, mots utilisés dans l'article, liens hypertexte, date de publication, etc. Ces données sont ensuite stockées via un moteur d'indexation pour permettre leur exploitation ultérieure parmi des centaines de milliers de données provenant d'autres articles.


Installation
============

Heraldic est développé en Python 3.6+. L'utilisation de **pipenv** est conseillée pour installer automatiquement les dépendances contenues dans le fichier *Pipfile.lock* :

.. code-block:: bash

    git clone https://github.com/Tagazoc/Heraldic
    cd heraldic
    pipenv shell
    pipenv update


Configuration
=============

La configuration par défaut est présente dans le fichier *config/default.ini* :

.. code-block:: ini

    [DEFAULT]
    elasticsearch_host = 127.0.0.1  # Hôte elasticsearch
    elasticsearch_port = 9200       # Port elasticsearch
    extract_words = no              # Désactivation de l'extraction des mots des articles

La configuration locale s'effectue dans le fichier *config/config.ini* .

