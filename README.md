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
elasticsearch_port = 9200	# Port elasticsearch
extract_words = no		# Désactivation de l'extraction des mots des articles
```

La configuration locale s'effectue dans le fichier *config/config.ini* .

## Création des indexes

La création des indexes s'effectue par le biais du script *scripts/create_indices.py* .

## Récupération d'articles

La récupération d'articles par Heraldic s'effectue via un utilitaire en ligne de commande :::

    python -m heraldic <commande> [options]

Actuellement, il existe deux commandes :

* "*gather*", qui permet la récupération d'un article, ou une liste d'articles dans un fichier. L'aide complète est :

```bash
usage: heraldic gather [-h] (-f FILE | -i | -u [URL [URL ...]]) [-d DEPTH]
                       [-o] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File containing one or several URLs (one per line)
  -i, --stdin           Get URL from stdin
  -u [URL [URL ...]], --url [URL [URL ...]]
                        URL to gather
  -d DEPTH, --depth DEPTH
                        Depth of recursive gathering of sources
  -o, --override        Gather again up-to-date documents
  -t, --test            Stop on optional parsing exception
```

* "*harvest*", qui permet la récupération d'un flux RSS ou tous ceux qui sont enregistrés dans l'indexeur. L'aide complète est :

```bash
usage: heraldic harvest [-h] [-o] [-d DEPTH] [media]

positional arguments:
  media                 Specify only one media to harvest

optional arguments:
  -h, --help            show this help message and exit
  -o, --override        Gather again up-to-date documents
  -d DEPTH, --depth DEPTH
                        Depth of recursive gathering of sources
```

On remarque l'option *DEPTH* qui permet la récupération récursive des liens dans les articles, si ceux-ci sont supportés bien entendu.

Si l'extraction des mots est activée dans le fichier de configuration, la récupération d'articles utilise le parsing du modèle français par défaut, un modèle plus spécifique à Heraldic (correspondant mieux aux articles Web) n'étant pas encore disponible. Ce modèle français est récupérable avec la commande suivante :

```bash
python -m spacy download fr
```

