import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Modèle représentant un projet dans le système de gestion.

    Attributs :
        title (str) : Le titre du projet, limité à 128 caractères.
        description (str) : Une description détaillée du projet.
        type (str) : Le type du projet. Doit être l'une des options suivantes :
                     - BACKEND : Back-end
                     - FRONTEND : Front-end
                     - IOS : Application iOS
                     - ANDROID : Application Android
        author (User) : L'utilisateur Django qui a créé le projet.
        created_time (datetime) : Date et heure de création automatique du projet.
    """

    # Choix possibles pour le type de projet
    TYPE_CHOICES = [
        ("BACKEND", "Back-end"),
        ("FRONTEND", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    # Titre du projet
    title = models.CharField(max_length=128)
    # Description complète du projet
    description = models.TextField()
    # Type de projet avec contraintes sur les valeurs possibles
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    # Lien vers l'auteur (utilisateur Django)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_projects")
    # Date et heure de création automatique
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche le titre du projet dans l'administration ou console
        return self.title


class Contributor(models.Model):
    """
    Modèle représentant un contributeur à un projet.

    Attributs :
        user (User) : L'utilisateur qui contribue au projet.
        project (Project) : Le projet auquel l'utilisateur contribue.
        (optionnel) author (User) : L'utilisateur qui a ajouté ce contributeur.

    Contraintes :
        unique_together : Empêche un utilisateur d'être ajouté deux fois au même projet.
    """

    # L'utilisateur contributeur
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Le projet auquel l'utilisateur contribue
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    # Optionnel : qui a ajouté ce contributeur
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="added_contributors")

    class Meta:
        # Empêche la duplication d'un même utilisateur sur le même projet
        unique_together = ("user", "project")

    def __str__(self):
        # Affiche un format lisible : "utilisateur → projet"
        return f"{self.user.username} → {self.project.title}"


class Issue(models.Model):
    """
    Modèle représentant une issue (tâche, bug ou fonctionnalité) liée à un projet.

    Attributs :
        title (str) : Le titre de l’issue.
        description (str) : Description détaillée de l’issue.
        tag (str) : Catégorie de l’issue : Bug, Feature ou Task.
        priority (str) : Priorité de l’issue : Low, Medium, High.
        status (str) : Statut de l’issue : To Do, In Progress, Finished.
        project (Project) : Projet associé à l’issue.
        author (User) : Créateur de l’issue.
        assignee (User) : Utilisateur assigné pour résoudre l’issue.
        created_time (datetime) : Date et heure de création automatique.
    """

    # Choix possibles pour le type d’issue
    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]

    # Choix possibles pour la priorité
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    # Choix possibles pour le statut
    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    # Titre de l’issue
    title = models.CharField(max_length=128)
    # Description détaillée
    description = models.TextField()
    # Catégorie de l’issue
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    # Niveau de priorité
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    # Statut actuel, par défaut "TODO"
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="TODO")
    # Projet auquel l’issue appartient
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    # Créateur de l’issue
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_issues")
    # Utilisateur assigné à l’issue
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_issues")
    # Date et heure de création automatique
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche le titre de l’issue pour identification rapide
        return self.title


class Comment(models.Model):
    """
    Modèle représentant un commentaire sur une issue.

    Attributs :
        id (UUID) : Identifiant unique du commentaire.
        description (str) : Contenu du commentaire.
        issue (Issue) : L’issue associée à ce commentaire.
        author (User) : Utilisateur ayant écrit le commentaire.
        created_time (datetime) : Date et heure de création automatique.
    """

    # UUID unique pour identifier le commentaire
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Contenu du commentaire
    description = models.TextField()
    # L’issue à laquelle le commentaire est associé
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    # Auteur du commentaire
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    # Date et heure de création automatique
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche un résumé lisible : "Comment by user on issue"
        return f"Comment by {self.author.username} on {self.issue.title}"
