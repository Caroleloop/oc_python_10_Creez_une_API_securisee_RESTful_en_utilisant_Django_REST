from rest_framework import routers
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet
from django.urls import path, include

# Création d'un routeur par défaut fourni par DRF
# Ce routeur génère automatiquement les routes CRUD pour chaque ViewSet enregistré
router = routers.DefaultRouter()

# Enregistrement du ProjectViewSet dans le routeur
# - "projects" sera le préfixe de l'URL (exemple : /projects/)
# - DRF générera automatiquement les routes : list, create, retrieve, update, destroy
router.register(r"projects", ProjectViewSet)

# Enregistrement du ContributorViewSet dans le routeur
# - "contributors" sera le préfixe de l'URL (exemple : /contributors/)
router.register(r"contributors", ContributorViewSet)

# Enregistrement du IssueViewSet dans le routeur
# - "issues" sera le préfixe de l'URL (exemple : /issues/)
router.register(r"issues", IssueViewSet)

# Enregistrement du CommentViewSet dans le routeur
# - "comments" sera le préfixe de l'URL (exemple : /comments/)
router.register(r"comments", CommentViewSet)

# Définition des URL patterns accessibles depuis ce module
# L'inclusion de router.urls permet d'ajouter automatiquement toutes les routes générées
urlpatterns = [
    path("", include(router.urls)),  # Inclut toutes les URLs générées par le routeur
]
