from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur étendant le modèle par défaut d'authentification de Django.

    Attributs supplémentaires :
    - age (PositiveIntegerField) : Âge de l'utilisateur. Doit être un entier positif.
    - can_be_contacted (BooleanField) : Indique si l'utilisateur accepte d'être contacté (par email, notifications...).
    - can_data_be_shared (BooleanField) : Indique si les données de l'utilisateur peuvent être partagées (ex. à des fins statistiques).

    Hérite également de tous les champs et comportements du modèle AbstractUser :
    - username, email, password, first_name, last_name, etc.
    """

    age = models.PositiveIntegerField()  # Âge de l'utilisateur (doit être > 15)
    can_be_contacted = models.BooleanField(default=False)  # Consentement à être contacté
    can_data_be_shared = models.BooleanField(default=False)  # Consentement au partage des données
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["age"]

    def clean(self):
        """
        Valide que l'âge est strictement supérieur à 15.
        Appelée automatiquement lors des validations du modèle (ex : admin, formulaire, save(clean=True)...).
        """
        super().clean()
        if self.age <= 15:
            raise ValidationError({"age": "L'utilisateur doit avoir plus de 15 ans."})

    def __str__(self):
        """
        Retourne le nom d'utilisateur sous forme de chaîne.
        """
        return self.username
