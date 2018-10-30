Heraldic est un outil d'analyse de médias Web, ou plus précisément un outil d'agrégation de méta-données contenues dans des articles sur le Web. Ces méta-données sont notamment les mots utilisés (en utilisant la bibliothèque Python/Cython Spacy), les liens utilisés en tant que source des articles, les dates de publication et mise à jour, les mots-clés, etc.
Le langage utilisé est principalement **Python**, et la solution d'indexation utilisée est **Elasticsearch**.

Heraldic est entièrement libre (sous licence GNU AGPLv3) et a pour vocation d'être d'utilité publique, des exports de la base d'articles seront disponibles chaque jour.

# Installation
Heraldic est développé en Python 3.6+. L'utilisation de **pipenv** est conseillée pour installer automatiquement les dépendances contenues dans le fichier *Pipfile.lock* :

```bash
git clone https://github.com/Tagazoc/Heraldic
cd heraldic
pipenv shell
pipenv update
```

# Configuration

La configuration par défaut est présente dans le fichier *config/default.ini* :

```ini
[DEFAULT]
elasticsearch_host = 127.0.0.1	# Hôte elasticsearch
elasticsearch_port = 9200		# Port elasticsearch
extract_words = no				# Désactivation de l'extraction des mots des articles
```

La configuration locale s'effectue dans le fichier *config/config.ini* .

## Création des indexes

La création des indexes s'effectue par le biais du script *scripts/create_indices.py* .

## Récupération d'articles

Les différents fichiers du répertoire *samples/* emploient différentes manières de récupérer des articles :

* le script *single_extractor.py* récupère l'URL passée en entrée ou en argument.
* le script *harvest_url_list.py* récupère les URL présentes dans le fichier passé en argument.
* le script *harvest_feed.py* récupère tous les articles présents dans le flux RSS dont l'URL est passée en argument.
* le script *harvest_rss_feeds.py* récupère tous les articles des flux stockés dans l'indexeur. Ces flux doivent être déposés via le script *scripts/create_feeds.py* avec pour argument un fichier contenant tous les feeds à inclure.

Si l'extraction des mots est activée, la récupération d'articles utilise le parsing du modèle français par défaut, un modèle plus spécifique à Heraldic (correspondant mieux aux articles Web) n'étant pas encore disponible. Ce modèle français est récupérable avec la commande suivante :

```bash
python -m spacy download fr
```

