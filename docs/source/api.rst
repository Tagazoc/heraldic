API
===

Une API était nécessaire pour accéder aux données principales contenues dans l'indexeur, tout en restreignant la possibilité de faire des requêtes longues et complexes, sans parler des suppressions de contenu qui ne sont pas limitables avec la version open source de l'indexeur, lorsqu'on y a un accès direct.

Cette API est construite avec le framework Connexion et le standard de description OpenAPI. Elle se lance via le script ``heraldic/api/server.py`` .

Pour y accéder, il suffit d'accéder à l'adresse http://localhost:5000/api (le port est spécifié dans le script ``server.py``). La documentation complète de l'API est disponible sur l'UI Swagger disponible à l'adresse http://localhost:5000/api/ui , ainsi que des fonctionnalités de tests de chaque requête.


