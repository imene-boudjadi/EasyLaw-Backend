# Documentation du module Moderator Routes

Ce module définit plusieurs routes pour gérer les utilisateurs et les modérateurs.

## Dépendances

Ce module utilise Flask pour définir les routes, jsonify pour convertir les objets en JSON, et jwt pour gérer les tokens d'authentification.

## Décorateur admin_required

Le décorateur `admin_required` est utilisé pour s'assurer que seuls les utilisateurs avec le rôle d'administrateur peuvent accéder à certaines routes. Il extrait le token d'authentification de l'en-tête "Authorization", décode le token pour obtenir l'ID de l'utilisateur, puis vérifie que l'utilisateur a le rôle d'administrateur.

## Routes



D'accord, voici comment vous pourriez documenter vos fonctions en suivant le même format :

**Routes d'administration**

**Obtenir tous les utilisateurs**
- Url: /users
- Méthode: GET
- En-tête : Authorization Bearer {token}
- Corps de la requête: Non applicable
- Réponse:
  - Réponse en cas de succès:
    - success: true
    - data: [Objets utilisateur]
  - Réponse en cas d'erreur:
    - success: false
    - message: String

**Obtenir tous les modérateurs**
- Url: /moderators
- Méthode: GET
- En-tête : Authorization Bearer {token}
- Corps de la requête: Non applicable
- Réponse:
  - Réponse en cas de succès:
    - success: true
    - data: [Objets modérateur]
  - Réponse en cas d'erreur:
    - success: false
    - message: String

**Mettre à jour un modérateur**
- Url: /update_moderator?id={id}
- Méthode: POST
- En-tête : Authorization Bearer {token}
- Corps de la requête:
  - id: Int
  - username: String
  - password: String
  - niveau: Int
  - role: String
  - phoneNumber: Int
  - email: String
  - deleted: Boolean
- Réponse:
  - Réponse en cas de succès:
    - success: true
    - data: Objet du modérateur mis à jour
  - Réponse en cas d'erreur:
    - success: false
    - message: String

**Ajouter un modérateur**
- Url: /add_moderator
- Méthode: POST
- En-tête : Authorization Bearer {token}
- Corps de la requête:
  - id: Int
  - username: String
  - password: String
  - niveau: Int
  - role: String
  - phoneNumber: Int
  - email: String
  - deleted: Boolean
- Réponse:
  - Réponse en cas de succès:
    - success: true
    - data: Objet du modérateur créé
  - Réponse en cas d'erreur:
    - success: false
    - message: String
