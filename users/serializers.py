from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User.

    Ce serializer est utilisé pour :
    - convertir les objets `User` en JSON (et inversement),
    - gérer la validation des données,
    - appliquer des règles métier comme la vérification de l'âge minimum,
    - hasher le mot de passe lors de la création d'un nouvel utilisateur.

    Hérite de `serializers.ModelSerializer` pour générer automatiquement
    les champs en fonction du modèle `User`.
    """

    class Meta:
        """
        Classe interne Meta qui définit la configuration du serializer.

        Attributs :
            model (User) : le modèle Django lié à ce serializer.
            fields (list) : la liste des champs du modèle à inclure dans le serializer.
        """

        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_age(self, value):
        """
        Vérifie que l'utilisateur a plus de 15 ans.

        Args:
            value (int): l'âge fourni par l'utilisateur.

        Raises:
            serializers.ValidationError: si l'âge est inférieur ou égal à 15.

        Returns:
            int: l'âge validé s'il est correct.
        """
        if value <= 15:
            raise serializers.ValidationError("L'utilisateur doit avoir plus de 15 ans.")
        return value

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur en hashant correctement son mot de passe.

        Args:
            validated_data (dict): données validées pour la création de l'utilisateur.

        Returns:
            User: instance nouvellement créée et sauvegardée dans la base de données.
        """
        # On retire le mot de passe du dictionnaire validé pour le traiter séparément
        password = validated_data.pop("password", None)

        # Création d'une nouvelle instance User avec les autres champs
        user = self.Meta.model(**validated_data)

        # Si un mot de passe est fourni, on le hash avant de l'attribuer
        if password:
            user.set_password(password)  # sécurisation du mot de passe

        # Sauvegarde de l'utilisateur en base de données
        user.save()

        return user
