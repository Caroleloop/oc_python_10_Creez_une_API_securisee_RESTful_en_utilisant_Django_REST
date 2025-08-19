from rest_framework import viewsets, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.exceptions import PermissionDenied, ValidationError
from users.models import User


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributorOrAuthor(permissions.BasePermission):
    """
    Permission pour vérifier si l'utilisateur est l'auteur du projet
    ou un contributeur de ce projet.
    """

    def has_permission(self, request, view):
        # Création seulement pour les contributeurs/auteurs
        if request.method == "POST":
            project_id = request.data.get("project") or request.data.get("issue")

            if not project_id:
                return False

            from .models import Project, Issue, Contributor

            # Si c’est un commentaire, récupérer le projet via l’issue
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

            # Vérifie si user = auteur OU contributeur
            return (
                project.author == request.user
                or Contributor.objects.filter(project=project, user=request.user).exists()
            )
        return True


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Enregistre le projet avec l'utilisateur actuel comme auteur
        project = serializer.save(author=self.request.user)

        # Ajoute automatiquement l'auteur comme contributeur
        Contributor.objects.create(
            user=self.request.user, project=project, author=self.request.user  # il s’ajoute lui-même
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        project_type = self.request.query_params.get("type")
        if project_type:
            queryset = queryset.filter(type=project_type)
        # Tri par titre (ou tu peux changer le champ)
        queryset = queryset.order_by("title")
        return queryset


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Si on passe ?project=<id> dans l’URL,
        on filtre les contributeurs de ce projet uniquement.
        """
        queryset = super().get_queryset()
        project_id = self.request.query_params.get("project")
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        project_id = self.request.data.get("project")
        user_id = self.request.data.get("user")

        if not project_id or not user_id:
            raise ValidationError("Payload must contain 'project' and 'user' IDs.")

        # Fetch project
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError("Invalid project ID.")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("Invalid user ID.")

        # Only the project author can add contributors
        if project.author != self.request.user:
            raise PermissionDenied("Only the project author can add contributors.")

        # Optional: prevent duplicates
        if Contributor.objects.filter(project=project, user_id=user_id).exists():
            raise ValidationError("This user is already a contributor to the project.")

        # Save with enforced project and user
        serializer.save(project=project, user=user, author=project.author)

    def perform_destroy(self, instance):
        # Empêcher de supprimer l’auteur du projet
        if instance.project.author == instance.user:
            raise PermissionDenied("Impossible de supprimer l'auteur du projet.")
        instance.delete()


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsContributorOrAuthor]

    def get_queryset(self):
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
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly, IsContributorOrAuthor]

    def get_queryset(self):
        queryset = super().get_queryset()
        issue_id = self.request.query_params.get("issue")
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        # Trier par date de création
        queryset = queryset.order_by("created_time")
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
