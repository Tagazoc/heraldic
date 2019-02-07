Récupération d'articles
=======================

La récupération d'articles par Heraldic s'effectue via un utilitaire en ligne de commande :::

    python -m heraldic <commande> [options]

Actuellement, il existe deux commandes :

* "``gather``", qui permet la récupération d'un article, ou une liste d'articles dans un fichier. L'aide complète est : ::

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

* "``harvest``", qui permet la récupération d'un flux RSS ou tous ceux qui sont enregistrés dans l'indexeur. L'aide complète est : ::

    usage: heraldic harvest [-h] [-o] [-d DEPTH] [media]
    
    positional arguments:
      media                 Specify only one media to harvest
    
    optional arguments:
      -h, --help            show this help message and exit
      -o, --override        Gather again up-to-date documents
      -d DEPTH, --depth DEPTH
                            Depth of recursive gathering of sources

On remarque l'option ``DEPTH`` qui permet la récupération récursive des liens dans les articles, si ceux-ci sont supportés bien entendu.

* "``test``", qui permet la récupération simplifiée des articles spécifiés comme référence pour les différents extracteurs d'un ou de l'ensemble des médias supportés : ::

    usage: heraldic test [-h] [media]

    positional arguments:
      media       Specify only one media to test

    optional arguments:
      -h, --help  show this help message and exit

