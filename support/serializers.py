from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Contributor, Issue, Comment


# --- User simplifié (pour auteur/contributeurs/assignee) ---
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer simplifié pour représenter un utilisateur.

    Utilisé comme sous-serializer pour les auteurs, contributeurs ou assignees.
    Champs inclus :
    - id : identifiant unique de l'utilisateur
    - username : nom d'utilisateur
    - email : adresse email
    """

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]


# --- Commentaires imbriqués ---
class CommentNestedSerializer(serializers.ModelSerializer):
    """
    Serializer pour les commentaires, utilisé en mode imbriqué dans les issues.

    Inclut les informations de l'auteur sous forme de UserSerializer.
    Champs inclus :
    - id : identifiant du commentaire
    - description : contenu du commentaire
    - author : auteur du commentaire (UserSerializer)
    - created_time : date et heure de création
    """

    author = UserSerializer(read_only=True)  # Auteur en lecture seule

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "created_time"]


# --- Issues imbriquées (avec commentaires) ---
class IssueNestedSerializer(serializers.ModelSerializer):
    """
    Serializer pour les issues, utilisé en mode imbriqué dans les projets.

    Inclut :
    - author : auteur de l'issue (UserSerializer)
    - assignee : personne assignée à l'issue (UserSerializer)
    - comments : liste de commentaires (CommentNestedSerializer)
    Champs principaux :
    - id, title, description, tag, priority, status, created_time
    """

    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    comments = CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "created_time",
            "comments",
        ]


# --- Contributeurs imbriqués ---
class ContributorNestedSerializer(serializers.ModelSerializer):
    """
    Serializer pour les contributeurs d'un projet, utilisé en mode imbriqué.

    Inclut :
    - user : informations de l'utilisateur (UserSerializer)
    Champs principaux :
    - id, user
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user"]


# --- Serializer principal pour création/édition projet ---
class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création et la modification des projets.

    Champs :
    - Tous les champs du modèle Project
    Champs en lecture seule :
    - author : auteur du projet
    - created_time : date de création
    """

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["author", "created_time"]


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer allégé pour la liste des projets.
    N'affiche que les infos essentielles (pas de description ni détails).
    """

    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "title", "type", "author", "created_time"]


# --- Serializer détaillé pour affichage projet ---
class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour l'affichage complet d'un projet.

    Inclut :
    - author : auteur du projet (UserSerializer)
    - contributors : liste des contributeurs (ContributorNestedSerializer)
    - issues : liste des issues du projet (IssueNestedSerializer)
    Champs principaux :
    - id, title, description, type, created_time
    """

    author = UserSerializer(read_only=True)
    contributors = ContributorNestedSerializer(many=True, read_only=True)
    issues = IssueNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "author",
            "created_time",
            "contributors",
            "issues",
        ]


# --- Serializer contributeurs standard (API /contributors/) ---
class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour les contributeurs, utilisé dans les endpoints CRUD.

    - Permet de créer ou lister un contributeur.
    - Empêche un utilisateur d'être ajouté deux fois au même projet.
    """

    class Meta:
        model = Contributor
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}  # Champ author en lecture seule si présent

    def validate(self, data):
        """
        Validation personnalisée pour empêcher la duplication de contributeur dans le même projet.
        """
        if Contributor.objects.filter(user=data["user"], project=data["project"]).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        return data


# --- Serializer issues standard (API /issues/) ---
class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer standard pour les issues.

    - Utilisé pour les endpoints CRUD.
    - Champs en lecture seule :
      - author : auteur de l'issue
      - created_time : date de création
    """

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["author", "created_time"]


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour une issue (utilisé dans /issues/<id>/).
    Inclut les commentaires imbriqués + infos auteur/assignee.
    """

    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    comments = CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "author",
            "assignee",
            "created_time",
            "comments",
        ]


class IssueListSerializer(serializers.ModelSerializer):
    """
    Serializer allégé pour la liste des issues.
    N'affiche que les infos essentielles (pas de description ni commentaires).
    """

    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ["id", "title", "tag", "priority", "status", "author", "assignee", "created_time"]


# --- Serializer commentaires standard (API /comments/) ---
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer standard pour les commentaires.

    - Utilisé pour les endpoints CRUD.
    - Champs en lecture seule :
      - author : auteur du commentaire
      - created_time : date de création
    """

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created_time"]
