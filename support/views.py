from rest_framework import viewsets, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from rest_framework.exceptions import PermissionDenied


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


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

    def perform_destroy(self, instance):
        # Empêcher de supprimer l’auteur du projet
        if instance.project.author == instance.user:
            raise PermissionDenied("Impossible de supprimer l'auteur du projet.")
        instance.delete()


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

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
