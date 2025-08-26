# SoftDesk Support - API Backend

SoftDesk Support est une application de gestion et de suivi des problèmes techniques au sein de projets logiciels. Ce dépôt contient l'API RESTful sécurisée qui alimente l'application, développée avec Django et Django REST Framework.

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


## ⚙️ Installation avec Pipenv

1. Cloner le dépôt :
```bash
git clone https://github.com/<votre-repo>/softdesk-backend.git
cd softdesk-backend
```

2. Installer les dépendances et créer l’environnement virtuel :
```bash
pipenv install --dev
```

3. Activer l’environnement virtuel :
```bash
pipenv shell
```

4. Appliquer les migrations et lancer le serveur :
```bash
python manage.py migrate
python manage.py runserver
```


## 🚀 Usage

- Authentification via JWT (`/api/token/` et `/api/token/refresh/`)  
- Accès aux projets, issues et commentaires via les endpoints REST :
  - `/projects/`
  - `/issues/`
  - `/comments/`
  - `/contributors/`  
- Seuls les **contributeurs** peuvent consulter ou modifier un projet et ses issues/comments.


## 📝 Notes

- Recommandé : Python 3.11+, Django 4.x  
- API sécurisée et conforme aux bonnes pratiques REST  
- Pagination et filtres disponibles sur tous les endpoints de liste


## Auteurs

- **Carole Roch** _alias_ [@Caroleloop](https://github.com/Caroleloop)