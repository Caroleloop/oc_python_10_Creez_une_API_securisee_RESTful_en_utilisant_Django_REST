from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Récupère le modèle User utilisé par Django (cela permet de supporter les User personnalisés)
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet permettant de gérer les utilisateurs de l'application.

    Ce ViewSet fournit automatiquement les opérations CRUD (Create, Read, Update, Delete)
    grâce à l’héritage de `ModelViewSet`. Il utilise le modèle User défini dans l’application.

    Fonctionnalités principales :
    - Sérialisation avec `UserSerializer` pour transformer les objets User en JSON (et inversement).
    - Permissions définies pour autoriser toutes les requêtes (peut être adapté selon besoins).
    - Filtres disponibles pour permettre aux clients de filtrer les utilisateurs selon certains champs.

    Attributs :
        queryset (QuerySet): Ensemble de tous les utilisateurs.
        serializer_class (Serializer): Sérialiseur utilisé pour la transformation des objets User.
        permission_classes (list): Liste des permissions appliquées à ce ViewSet.
        filter_backends (list): Liste des backends de filtrage activés.
        filterset_fields (dict): Définition des champs et des opérateurs disponibles pour le filtrage.

    Champs filtrables :
        - age :
            * exact : âge exactement égal à la valeur
            * gt    : âge strictement supérieur
            * gte   : âge supérieur ou égal
            * lt    : âge strictement inférieur
            * lte   : âge inférieur ou égal
        - can_be_contacted (booléen) : si l’utilisateur accepte d’être contacté
        - can_data_be_shared (booléen) : si l’utilisateur accepte que ses données soient partagées
    """

    # Définition de la source de données (tous les utilisateurs en base)
    queryset = User.objects.all()

    # Sérialiseur utilisé pour la conversion User <-> JSON
    serializer_class = UserSerializer

    # Permissions : ici tout le monde peut accéder (à adapter en fonction du projet)
    permission_classes = [permissions.AllowAny]

    # Active le filtrage basé sur django-filters
    filter_backends = [DjangoFilterBackend]

    # Définit les champs sur lesquels un filtrage est possible
    filterset_fields = {
        "age": ["exact", "gt", "gte", "lt", "lte"],  # filtres numériques sur l'âge
        "can_be_contacted": ["exact"],  # filtrage booléen (True/False)
        "can_data_be_shared": ["exact"],  # filtrage booléen (True/False)
    }

    def get_queryset(self):
        return User.objects.all().prefetch_related(
            "authored_projects", "assigned_issues", "authored_issues", "comments"
        )
