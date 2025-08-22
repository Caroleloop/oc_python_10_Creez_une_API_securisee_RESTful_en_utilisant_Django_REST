from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


# Création d'un routeur par défaut fourni par DRF.
# Ce routeur génère automatiquement les routes REST basées sur le ViewSet fourni.
router = DefaultRouter()

# Enregistrement du UserViewSet dans le routeur.
# - "users" sera le préfixe de l'URL (par exemple /users/).
# - `basename="user"` permet de nommer les routes (ex: "user-list", "user-detail").
router.register(r"users", UserViewSet, basename="user")

# Définition de la liste des URLs accessibles depuis ce module.
# On inclut ici toutes les routes générées par le routeur.
urlpatterns = [
    path("", include(router.urls)),  # Inclut toutes les URLs générées par le routeur
]
