from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur qui étend le modèle d'authentification
    par défaut de Django (AbstractUser).

    Ce modèle ajoute des champs spécifiques en plus de ceux hérités :
    - age (PositiveIntegerField) : Âge de l'utilisateur. Doit être un entier strictement positif et supérieur à 15.
    - can_be_contacted (BooleanField) : Détermine si l'utilisateur accepte d'être contacté (emails, notifications...).
    - can_data_be_shared (BooleanField) : Détermine si l'utilisateur accepte que ses données soient partagées
      (ex. à des fins statistiques ou d'analyse).
    - email (EmailField) : Adresse email unique de l'utilisateur (contrainte d'unicité ajoutée).

    Champs hérités de AbstractUser :
    - username : Identifiant unique de connexion.
    - first_name : Prénom de l'utilisateur.
    - last_name : Nom de l'utilisateur.
    - password : Mot de passe haché.
    - is_staff, is_active, date_joined, etc.

    Attributs de configuration :
    - REQUIRED_FIELDS (list) : Champs requis en plus de `username` et `password` lors de la création d’un
      superutilisateur.
    """

    age = models.PositiveIntegerField()  # Âge de l'utilisateur (doit être > 15)
    can_be_contacted = models.BooleanField(default=False)  # Indique si l'utilisateur accepte d'être contacté
    can_data_be_shared = models.BooleanField(
        default=False
    )  # Indique si l'utilisateur accepte le partage de ses données
    email = models.EmailField(unique=True)  # Adresse email unique pour chaque utilisateur

    # Spécifie les champs supplémentaires requis pour la création d’un superutilisateur
    REQUIRED_FIELDS = ["age"]

    def clean(self):
        """
        Effectue des validations personnalisées sur le modèle.

        Vérifie que :
        - L'âge de l'utilisateur est strictement supérieur à 15.

        Lève une ValidationError si la condition n'est pas respectée.

        Cette méthode est automatiquement appelée lors :
        - des validations de formulaires (ModelForm, admin Django)
        - de l'appel explicite à `full_clean()`
        - lors de l’enregistrement si `save(clean=True)` est utilisé.
        """
        super().clean()
        if self.age <= 15:
            raise ValidationError({"age": "L'utilisateur doit avoir plus de 15 ans."})

    def __str__(self):
        """
        Représentation textuelle de l'utilisateur.

        Retourne :
        - str : Le nom d'utilisateur (username), utilisé dans l’admin Django,
          les logs et lors des affichages par défaut.
        """
        return self.username
