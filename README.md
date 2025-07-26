# SoftDesk Support - API Backend

SoftDesk Support est une application B2B de gestion et de suivi des problèmes techniques au sein de projets logiciels. Ce dépôt contient l'API RESTful sécurisée qui alimente l'application, développée avec Django et Django REST Framework.

## 📦 Fonctionnalités principales

- Authentification JWT
- Gestion des utilisateurs avec consentement RGPD
- Gestion des projets et des contributeurs
- Création et gestion des issues (problèmes/tâches)
- Ajout de commentaires liés aux issues
- Système de permissions basé sur les rôles
- Pagination des ressources pour améliorer la performance
- Respect des normes de sécurité OWASP
- Conception green code (code sobre et optimisé)

## 🧱 Modèles de données

- **User** : Utilisateur inscrit avec `username`, `password`, `age`, `can_be_contacted`, `can_data_be_shared`
- **Project** : Projet avec `title`, `description`, `type` (back-end, front-end, iOS, Android)
- **Contributor** : Lien entre un utilisateur et un projet
- **Issue** : Tâche ou bug avec `title`, `description`, `priority`, `tag`, `status`, `assigned_to`
- **Comment** : Commentaire lié à une issue avec `description` et UUID

## 🔐 Sécurité

### Authentification & Autorisation
- Utilisation de JWT pour toutes les opérations sécurisées
- Accès restreint aux ressources :
  - Seuls les contributeurs d’un projet peuvent consulter et modifier ses données
  - Seuls les auteurs peuvent modifier ou supprimer leurs ressources

### RGPD
- Vérification de l’âge (minimum 15 ans)
- Consentement explicite requis pour :
  - Être contacté (`can_be_contacted`)
  - Partager ses données (`can_data_be_shared`)
- Accès, modification et suppression des données personnelles autorisés

### OWASP Top 10
- Protection contre les failles courantes (A1 à A10)
- Mise en place des concepts AAA : Authentification, Autorisation, Traçabilité

## 🌿 Green Code

- Utilisation de la pagination sur toutes les ressources listées
- Code structuré pour limiter la charge serveur
- Optimisation des requêtes et dépendances (Pipenv ou Poetry recommandé)