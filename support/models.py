import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Représente un projet dans le système.

    Attributs :
        title (str) : Le titre du projet.
        description (str) : Une description détaillée du projet.
        type (str) : Le type du projet (Back-end, Front-end, iOS, Android).
        author (User) : L'utilisateur qui a créé le projet.
        created_time (datetime) : La date et l'heure de création du projet.
    """

    TYPE_CHOICES = [
        ("BACKEND", "Back-end"),
        ("FRONTEND", "Front-end"),
        ("IOS", "iOS"),
        ("ANDROID", "Android"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_projects")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche le titre du projet dans l’interface d’administration ou lors d’une impression
        return self.title


class Contributor(models.Model):
    """
    Représente l'association entre un utilisateur et un projet auquel il contribue.

    Attributs :
        user (User) : L'utilisateur contributeur.
        project (Project) : Le projet auquel l'utilisateur contribue.
        # author (User) : L'utilisateur qui a ajouté ce contributeur (par exemple le créateur du projet).
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributors")
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="added_contributors")

    class Meta:
        # Empêche qu’un même utilisateur soit ajouté deux fois à un même projet
        unique_together = ("user", "project")

    def __str__(self):
        # Affiche le lien utilisateur → projet
        return f"{self.user.username} → {self.project.title}"


class Issue(models.Model):
    """
    Représente une tâche, fonctionnalité ou bug liée à un projet.

    Attributs :
        title (str) : Le titre de l’issue.
        description (str) : Une description détaillée de l’issue.
        tag (str) : Le type d’issue (Bug, Feature, Task).
        priority (str) : Le niveau de priorité (Low, Medium, High).
        status (str) : Le statut de l’issue (To Do, In Progress, Finished).
        project (Project) : Le projet auquel l’issue appartient.
        author (User) : L’auteur de l’issue.
        assignee (User) : L’utilisateur assigné à l’issue.
        created_time (datetime) : La date et l’heure de création.
    """

    TAG_CHOICES = [
        ("BUG", "Bug"),
        ("FEATURE", "Feature"),
        ("TASK", "Task"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    STATUS_CHOICES = [
        ("TODO", "To Do"),
        ("IN_PROGRESS", "In Progress"),
        ("FINISHED", "Finished"),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="TODO")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_issues")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_issues")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche le titre de l’issue
        return self.title


class Comment(models.Model):
    """
    Représente un commentaire lié à une issue.

    Attributs :
        id (UUID) : Identifiant unique du commentaire.
        description (str) : Contenu du commentaire.
        issue (Issue) : L’issue concernée par le commentaire.
        author (User) : L’utilisateur ayant écrit le commentaire.
        created_time (datetime) : Date et heure de création du commentaire.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Affiche un résumé du commentaire
        return f"Comment by {self.author.username} on {self.issue.title}"
