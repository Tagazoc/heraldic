Extraction
==========

Processus
^^^^^^^^^
Le processus d'extraction des données consiste simplement en la lecture du code HTML de la page contenant un article, et la récupération de données précises placées à divers endroits de ce code. Comme chaque site a une façon de présenter et de coder les données différente, ce processus est spécifique à chaque média ; le média concerné est déduit du domaine présent dans l'URL, après vérification de celle-ci comme valide et supportée. Un même média peut être déployé sur plusieurs domaines et surtout sous-domaines ; cependant, il peut y avoir plusieurs styles de pages au sein d'un même domaine. Un média dans Heraldic peut donc concerner plusieurs domaines et proposer plusieurs extracteurs ; un extracteur est composé d'une collection de fonctions pour extraire les données des articles lui correspondant.

Lorsqu'il y a plusieurs extracteurs, le choix est effectué en testant la présence d'un élément spécifique au style de page concerné par chaque extracteur. Une fois l'extracteur choisi (ou s'il n'y en a qu'un) l'extraction peut réellement commencer. Elle débute par l'extraction des attributs obligatoires, sans lesquels les données du document ne seront pas indexées, par exemple le corps de l'article (qui ne sera pas directement indexé, mais est nécessaire à la récupération de nombreux autres attributs), et se poursuit par l'extraction des autres attributs. Chaque erreur d'extraction est enregistrée afin de permettre sa correction ultérieure.

Attributs à extraire
^^^^^^^^^^^^^^^^^^^^

L'ajout d'un média dans Heraldic s'effectue par l'analyse des différents styles de pages présents sur le ou les sites Web de ce média. Il faut faire une copie du fichier canevas heraldic/media/pattern.py et renseigner les informations suivantes :

Classe "`Media`" : Elle comprend les informations de base qui concernent le média.

* ``supported_domains`` : la liste des domaines liés à ce média.
* ``id`` : l'identifiant utilisé en base. Il s'agit généralement du nom du média, en minuscule, avec des tirets bas (ou underscore : _ ) pour remplacer les espaces ou ponctuations.
* ``display_name`` : le nom du média. 
* ``articles_regex`` : une liste d'expressions régulières permettant d'identifier au mieux l'URL d'un article (en opposition avec d'autres pages du site qui n'en sont pas). Cela peut concerner une extension, un identifiant numérique, etc.

Classe "`Extracteur`" : Comme son nom l'indique, elle contient les méthodes permettant l'extraction. Elle est spécifique à un style de page et il peut y en avoir plusieurs. Lorsque c'est le cas, il faut implémenter la méthode \_check\_extraction qui doit renvoyer (comme booléen) la présence ou non d'un élément du code HTML spécifique au style de page concerné.

Les autres méthodes à implémenter correspondent aux attributs extractibles du document, avec pour nom "``_extract_<nom de l'attribut>``". Certains attributs sont généralement implémentés de la même manière (dans la classe parente GenericExtractor) et n'ont pas besoin d'être réimplémentés, les autres doivent l'être. Les attributs sont :

* ``body`` (obligatoire) : Le corps effectif de l'article, sans le titre, éventuellement avec les légendes des images. Les contenus ajoutés par le site (liens d'actualité, publicités) doivent être supprimés, sauf s'il s'agit bien sûr de sources directement liées à l'article. Un traitement supplémentaire supprime automatiquement certaines balises internes telles que les balises "script". Cet attribut n'est pas directement indexé, mais il est conservé dans l'attribut de la classe "\_body\_tag" qui peut être accédé dans d'autres méthodes d'extraction.
* ``title`` : Le titre de l'article. L'intégration des articles avec les réseaux sociaux et les sites d'agrégation de contenus de presse fait que cette donnée est toujours implémentée de la même manière, sauf exception. On tentera de ne pas retenir le nom du média, qui peut être inséré dans le titre.
* ``description`` : La description de l'article : il s'agit généralement d'une méta-donnée qui n'est pas systématiquement affichée sur la page. Comme pour le titre, il y a rarement besoin de réimplémenter son extraction.
* ``category`` : La catégorie de l'article selon le site Web. Cela peut ainsi être aussi bien "Actualité" que "Monde" ou "Cuisine". On trouve généralement cette donnée dans une barre de navigation (souvent appelée "navbar").
* ``doc_publication_time`` : La date et l'heure de publication de l'article (à ne pas confondre avec gather\_time, la date de récupération par Heraldic). On pourrait penser que cette donnée est aussi standardisée que le titre ou la description, mais ce n'est pas le cas : il y a ainsi quatre façons différentes de l'extraire qui sont implémentées dans la classe parente. Cela couvre néanmoins la plupart des sites d'information.
* ``doc_update_time`` : La date et l'heure de mise à jour de l'article sur le site (à ne pas confondre avec update\_time, la date de mise à jour dans Heraldic). Elle est optionnelle et suit généralement la façon de faire de la date de publication.
* ``keywords`` : Les mots-clés associés par le site à l'article. Ils peuvent être nombreux, car ils interviendront dans le référencement sur les moteurs de recherche. C'est une méta-donnée qui ne nécessite généralement pas de réimplémentation.
* ``href_sources`` : Les liens placés en source de l'article, généralement situés directement dans le corps de l'article. Il convient de bien distinguer les sources de l'article des liens qui ne sont que des références vers d'autres endroits du site (par exemple un lien sur le nom d'une personnalité, pointant vers une page contenant une liste d'articles sur cette personnalité), et surtout des liens ajoutés du type "Lisez aussi". Ces derniers peuvent être conservés dans l'attribut de classe "\_side\_links" en vue de récupérer d'autres articles qui pourraient être absents d'Heraldic. Un traitement supplémentaire simplifie l'extraction : il faut juste récupérer les balises "a" caractérisant les liens dans la fonction d'extraction.
* ``news_agency`` : L'agence de presse à l'origine de la dépêche qui donne lieu à l'article, si elle existe bien évidemment. Généralement AFP, ou Reuters. Chaque média écrit cette information à l'endroit qu'il souhaite (avec le nom de l'auteur par exemple) mais toujours au même endroit.
* ``subscribers_only`` : Si oui ou non l'article est réservé aux abonnés ; dans ce cas, les quelques lignes qui sont généralement proposées gratuitement pourront être identifiées comme n'étant pas l'article complet.
* ``document_type`` : le type de document, pour le moment "article", "video" ou "panorama".
* ``side_links`` : Les liens dans un article vers d'autres articles du même média, qui ne sont pas des sources de cet article. Leur extraction est généralement effectuée avec celle de l'attribut href\_sources.



