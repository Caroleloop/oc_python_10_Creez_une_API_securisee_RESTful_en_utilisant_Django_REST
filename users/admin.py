from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Classe d’administration personnalisée pour le modèle `User`.

    Hérite de `UserAdmin` de Django et ajoute des champs personnalisés
    aux sections `fieldsets` (modification d’un utilisateur) et `add_fieldsets`
    (ajout d’un utilisateur).

    Attributs :
        fieldsets (tuple) :
            Définit les sections et champs affichés lors de la modification
            d’un utilisateur dans l’admin. On reprend les `fieldsets` de base
            de Django et on y ajoute :
            - age
            - can_be_contacted
            - can_data_be_shared

        add_fieldsets (tuple) :
            Définit les sections et champs affichés lors de l’ajout d’un
            utilisateur. On reprend ceux de Django et on y ajoute les mêmes
            champs personnalisés.
    """

    # Champs supplémentaires affichés lors de la modification d’un utilisateur
    fieldsets = UserAdmin.fieldsets + (
        (
            None,  # Pas de titre spécifique pour ce groupe
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )

    # Champs supplémentaires affichés lors de la création d’un utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,  # Pas de titre spécifique pour ce groupe
            {
                "fields": (
                    "age",
                    "can_be_contacted",
                    "can_data_be_shared",
                )
            },
        ),
    )
