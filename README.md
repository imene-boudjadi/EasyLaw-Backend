# Documentation du module Moderator Routes

Ce module définit plusieurs routes pour gérer les utilisateurs et les modérateurs.

## Dépendances

Ce module utilise Flask pour définir les routes, jsonify pour convertir les objets en JSON, et jwt pour gérer les tokens d'authentification.

## Décorateur admin_required

Le décorateur `admin_required` est utilisé pour s'assurer que seuls les utilisateurs avec le rôle d'administrateur peuvent accéder à certaines routes. Il extrait le token d'authentification de l'en-tête "Authorization", décode le token pour obtenir l'ID de l'utilisateur, puis vérifie que l'utilisateur a le rôle d'administrateur.

## Routes

- **/users [GET]** : Cette route renvoie une liste paginée d'utilisateurs. Les paramètres `page` et `per_page` peuvent être fournis dans la chaîne de requête pour contrôler la pagination.

- **/moderators [GET]** : Cette route renvoie une liste de modérateurs.

- **/delete_user [POST]** : Cette route supprime un utilisateur spécifié par l'ID dans la chaîne de requête.

- **/add_moderator [POST]** : Cette route ajoute un nouveau modérateur. Les détails du modérateur sont fournis dans le corps de la requête au format JSON.

- **/update_moderator [POST]** : Cette route met à jour un modérateur existant. Les détails du modérateur sont fournis dans le corps de la requête au format JSON.

Toutes ces routes nécessitent que l'utilisateur soit un administrateur, comme indiqué par le décorateur `@admin_required`.
