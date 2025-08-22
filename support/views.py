from rest_framework import viewsets, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
    ProjectDetailSerializer,
)
from rest_framework.exceptions import PermissionDenied, ValidationError
from users.models import User


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet aux utilisateurs de lire les objets,
    mais n'autorise la modification (PUT, PATCH, DELETE) qu'à l'auteur de l'objet.
    """

    def has_object_permission(self, request, view, obj):
        # Autoriser toutes les méthodes de lecture (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Vérifier si l'utilisateur connecté est bien l'auteur
        return obj.author == request.user


class IsContributorOrAuthor(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est l'auteur du projet
    ou un contributeur de ce projet.
    Utilisée notamment lors de la création d'issues ou de commentaires.
    """

    def has_permission(self, request, view):
        # Appliquer la logique uniquement lors d'une création (POST)
        if request.method == "POST":
            # Récupérer l'identifiant du projet ou de l'issue
            project_id = request.data.get("project") or request.data.get("issue")

            if not project_id:
                return False

            # Si l'objet est un commentaire → récupérer le projet via l'issue
            if view.basename == "comment":
                try:
                    issue = Issue.objects.get(id=project_id)
                    project = issue.project
                except Issue.DoesNotExist:
                    return False
            else:
                try:
                    project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return False

            # Vérifie si l'utilisateur est l'auteur ou un contributeur
            return (
                project.author == request.user
                or Contributor.objects.filter(project=project, user=request.user).exists()
            )
        # Pour les autres méthodes (GET, etc.), autoriser
        return True


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets :
    - Liste et détail
    - Création, modification et suppression
    - Filtrage par type
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Lors de la création d’un projet :
        - Associer l’auteur automatiquement à l’utilisateur connecté
        - Ajouter l’auteur comme contributeur par défaut
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    def get_queryset(self):
        """
        Personnalise la récupération des projets :
        - Filtrage par type si fourni (?type=)
        - Tri par titre
        """
        queryset = super().get_queryset()
        project_type = self.request.query_params.get("type")
        if project_type:
            queryset = queryset.filter(type=project_type)
        return queryset.order_by("title")

    def get_serializer_class(self):
        """
        Utiliser un serializer détaillé pour la liste et la consultation,
        sinon le serializer de base pour création/modification.
        """
        if self.action in ["retrieve", "list"]:
            return ProjectDetailSerializer
        return ProjectSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les contributeurs d’un projet :
    - Lister, ajouter ou supprimer des contributeurs
    - Filtrage possible par projet
    - Uniquement l’auteur du projet peut ajouter/supprimer
    """

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtrer les contributeurs d’un projet si ?project=<id> est fourni.
        """
        queryset = super().get_queryset()
        project_id = self.request.query_params.get("project")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        """
        Lors de l’ajout d’un contributeur :
        - Vérifie que le projet et l’utilisateur existent
        - Vérifie que l’auteur du projet est bien celui qui ajoute
        - Empêche les doublons
        """
        project_id = self.request.data.get("project")
        user_id = self.request.data.get("user")

        if not project_id or not user_id:
            raise ValidationError("Payload must contain 'project' and 'user' IDs.")

        # Vérifie que le projet existe
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError("Invalid project ID.")

        # Vérifie que l'utilisateur existe
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Invalid user ID.")

        # Vérifie que seul l’auteur du projet peut ajouter un contributeur
        if project.author != self.request.user:
            raise PermissionDenied("Only the project author can add contributors.")

        # Vérifie que le contributeur n’existe pas déjà
        if Contributor.objects.filter(project=project, user_id=user_id).exists():
            raise ValidationError("This user is already a contributor to the project.")

        # Enregistre le contributeur
        serializer.save(project=project, user=user)

    def perform_destroy(self, instance):
        """
        Lors de la suppression d’un contributeur :
        - Empêche la suppression de l’auteur du projet
        """
        if instance.project.author == instance.user:
            raise PermissionDenied("Impossible de supprimer l'auteur du projet.")
        instance.delete()


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les issues (tickets) liées aux projets :
    - Création, modification, suppression
    - Filtrage par projet, tag, statut, assignee ou priorité
    """

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsContributorOrAuthor]

    def get_queryset(self):
        """
        Permet de filtrer les issues selon différents critères :
        - ?project=<id>
        - ?tag=<valeur>
        - ?status=<valeur>
        - ?assignee=<id>
        - ?priority=<valeur>
        """
        queryset = super().get_queryset()
        project_id = self.request.query_params.get("project")
        tag = self.request.query_params.get("tag")
        status = self.request.query_params.get("status")
        assignee = self.request.query_params.get("assignee")
        priority = self.request.query_params.get("priority")

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if tag:
            queryset = queryset.filter(tag=tag)
        if status:
            queryset = queryset.filter(status=status)
        if assignee:
            queryset = queryset.filter(assignee_id=assignee)
        if priority is not None:
            queryset = queryset.filter(priority=priority.upper())

        return queryset

    def perform_create(self, serializer):
        """
        Lors de la création d’une issue :
        - Vérifie que l’assignee est bien auteur ou contributeur du projet
        - Définit l’auteur automatiquement comme l’utilisateur connecté
        """
        project = serializer.validated_data["project"]
        assignee = serializer.validated_data["assignee"]

        is_contributor = Contributor.objects.filter(project=project, user=assignee).exists()
        if not (project.author == assignee or is_contributor):
            raise ValidationError("L'assignee doit être auteur ou contributeur du projet.")

        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Lors de la mise à jour d’une issue :
        - Vérifie que l’assignee appartient bien au projet
        """
        project = serializer.validated_data.get("project", serializer.instance.project)
        assignee = serializer.validated_data.get("assignee", serializer.instance.assignee)

        is_contributor = Contributor.objects.filter(project=project, user=assignee).exists()
        if not (project.author == assignee or is_contributor):
            raise ValidationError("L'assignee doit être auteur ou contributeur du projet.")

        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires liés aux issues :
    - Création, modification, suppression
    - Filtrage par issue
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsContributorOrAuthor]

    def get_queryset(self):
        """
        Filtrer les commentaires d’une issue si ?issue=<id> est fourni.
        Trie les résultats par date de création.
        """
        queryset = super().get_queryset()
        issue_id = self.request.query_params.get("issue")
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset.order_by("created_time")

    def perform_create(self, serializer):
        """
        Lors de la création d’un commentaire :
        - Définit automatiquement l’auteur comme l’utilisateur connecté
        """
        serializer.save(author=self.request.user)
