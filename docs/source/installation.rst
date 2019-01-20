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

