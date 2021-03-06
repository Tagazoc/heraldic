Documents
=========

Dans Heraldic, un document représente un contenu sur une page Web. Cela est généralement un article, mais cela peut aussi concerner un diaporama ou une page dédiée à une vidéo. Le processus de récupération d'un document est bien précis afin de minimiser la probabilité de doublon de documents dans l'indexeur.

Processus de récupération d'une URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vérification du support du domaine
__________________________________


La matière première pour la récupération d'un article est son URL, ou une autre URL qui redirige sur cette URL. La première vérification (outre l'intégrité de cette URL) est le support du domaine : il n'est pas question de permettre à quiconque de requêter n'importe quel site de la toile via Heraldic. Le domaine doit donc être utilisé par un média supporté par l'outil (par exemple : ``www.lefigaro.fr``), ou un redirecteur accepté, qu'il soit spécifique (``lemde.fr`` est le générateur d'URL courtes du Monde) ou plus générique (bit.ly est à envisager).


Il y a là un point important à noter ; il n'est pas envisageable, ni souhaitable, de pouvoir requêter n'importe quel article provenant de n'importe quel site Web, mais uniquement les sites sur lesquels un travail d'extraction a été effectué. Pourquoi ? Parce qu'il y a bien des manières de développer un site, ce qui rend de nombreuses données difficiles à récupérer sans une recherche humaine préalable ; et on ne saurait prendre l'intégralité des données présentes sur la page HTML que l'on récupère : ainsi, énormément de sites d'information insèrent des liens vers d'autres articles autour et à l'intérieur du corps même de l'article, pour provoquer la poursuite de la lecture vers un autre article. Il faut donc pouvoir identifier ces contenus qui ne doivent pas être considérés comme des sources. Par ailleurs, certaines données ne sont absolument pas normalisées et dépendent entièrement de l'équipe qui a créé le site web (par exemple, l'AFP doit être cité lorsqu'un article provient d'une dépêche, mais l'emplacement de cette donnée semble être totalement libre).

Ainsi le domaine est vérifié ; ensuite, on recherche la présence de cette URL dans l'indexeur. On s'affranchira du protocole utilisé (HTTP ou HTTPS), ainsi que des données "supplémentaires" que l'on peut trouver dans une URL : paramètres, port du serveur, balises. Si le document existe, on procèdera alors à sa mise à jour ; sinon, c'est un nouveau document qui sera stocké.

Redirections 
____________

Seulement à ce moment, l'URL (simplifiée) est collectée (avec la méthode HTTP "GET") mais les vérifications ne sont pas terminées : il faut prévoir le cas où l'URL génère une ou plusieurs redirections, et vérifier l'URL de la cible. Une fois encore, on vérifie donc le domaine mais aussi la présence ou non de l'URL au sein de l'indexeur ; on vérifie aussi éventuellement la ressource de l'URL (``/guerre/les-guerres-sont-elles-justes.html``) pour voir si cela correspond bien à la façon de faire du site de référencer les articles, et si cela n'est pas une autre page sans contenu journalistique (par exemple un recueil comme ``/dossier/guerre/``). 

Extraction
__________

Alors l'extracteur correspondant au site Web est identifié, puis commence le processus d'extraction ; chaque donnée considérée comme intéressante et référencée sur le site est récupérée.
Comme chaque extracteur est créé par un être humain, il arrive fréquemment que l'extraction de certaines données se solde par une erreur. On distingue les données obligatoires qui empêchent complètement le stockage du document, et les données optionnelles qui le permettent tout de même. Néanmoins, ces erreurs sont stockées dans l'indexeur afin de pouvoir remédier ultérieurement au problème d'extraction et récupérer de nouveau le document.

Stockage
________

Les données sont alors stockées dans l'indexeur. Si l'URL existait déjà, on considère son évolution : si aucune donnée n'a évolué, rien n'est modifié. Si en revanche une ou plusieurs données ont été modifiées, le document existant dans l'indexeur est écrasé mais les anciennes données sont tout de même stockées dans l'indexeur à un autre endroit ; ainsi, pour un article mis à jour toute la journée et récupéré à chaque heure, il est possible d'avoir les données pour chacune des versions.


