Indexation
==========

Concepts
^^^^^^^^

Une fois qu'un article a été récupéré et que ses attributs ont été extraits de son contenu, ces derniers sont stockés dans une solution d'indexation, à savoir Elasticsearch. C'est un produit open source, qui dispose de fonctionnalités payantes comme le contrôle d'accès. Ce projet étant conduit avec quasiment aucune dépense financière, il n'est pas envisageable (en termes de fonctionnalité payantes, donc, mais aussi de puissance de serveur) de permettre à tout ceux qui le souhaitent d'accéder à notre instance Elasticsearch ; c'est notamment pour cette raison qu'il y a une API spécifique à Heraldic.

L'idée générale est donc d'encourager chacun souhaitant jouer comme il le souhaite avec toutes les données (plus que via l'API) à déployer une machine virtuelle avec une instance Elasticsearch. Pour comparaison, notre instance actuelle d'Elasticsearch tourne sur une distribution CentOS 7 hébergée sur un VPS avec deux coeurs, 4 Go de mémoire vive et 20 Go de mémoire SSD.

Tout le contenu indexé sera disponible en ligne et pourra être synchronisé avec un script, sur un modèle d'une sauvegarde complète chaque semaine et une sauvegarde incrémentale chaque jour. Ainsi, il sera très simple d'obtenir un environnement rigoureusement identique à celui de référence. En outre, cela permettra à quiconque souhaite utiliser la solution pour ses propres données et articles, de le faire sans rendre pour autant ces données publiques.

Indexes
^^^^^^^

On trouve différents index correspondant à différents types d'objets à indexer :

* ``docs`` : L'index principal, qui contient les données correspondant aux attributs des documents récupérés.
* ``docs_history`` : L'index contenant les anciennes versions des attributs des documents mis à jour. Par exemple, si le titre d'un document est mis à jour, sa récupération par Heraldic modifiera le document dans l'index docs et créera un document dans l'index docs_history contenant uniquement le titre avant modification (ainsi que la date de la précédente version).
* ``errors`` : L'index contenant les erreurs générées durant l'extraction d'attributs suite à la récupération d'une URL. On y trouve des erreurs liées à des documents existants dans l'index docs, mais aussi des erreurs sur des documents qui n'ont pas du tout été indexés à cause de l'échec de l'extraction d'un attribut obligatoire.
* ``feeds`` : L'index contenant les feeds utilisés pour la récupération des articles via des flux RSS. On y conserve la date et l'heure du dernier accès au flux, afin de ne pas parcourir l'ensemble du flux RSS s'il n'a pas été mis à jour depuis.



La création des indexes n'est en soi pas obligatoire pour l'indexation des documents, néanmoins elle est requise pour spécifier les types des propriétés des objets indexés (mapping). Pour ce faire, il suffit de lancer le script "``heraldic/scripts/create_indices.py``".

La création des feeds se fait via un autre script, "``heraldic/scripts/create_feeds.py``", en utilisant un fichier CSV contenant la paire "identifiant du média;URL du feed" pour chaque feed.
