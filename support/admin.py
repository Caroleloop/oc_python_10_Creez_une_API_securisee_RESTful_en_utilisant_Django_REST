from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


# ---------------------------------------------------------------------
# Inline pour les contributeurs
# ---------------------------------------------------------------------
class ContributorInline(admin.TabularInline):
    """
    Classe permettant d'afficher les contributeurs d'un projet directement
    dans l'interface admin du projet sous forme de tableau.

    Attributs :
        model (Model) : le modèle à utiliser pour cet inline (ici Contributor)
        extra (int)   : nombre de lignes vides supplémentaires à afficher
                        par défaut (0 signifie aucune ligne vide)
    """

    model = Contributor
    extra = 0  # Pas de lignes vides supplémentaires


# ---------------------------------------------------------------------
# Inline pour les issues
# ---------------------------------------------------------------------
class IssueInline(admin.TabularInline):
    """
    Classe permettant d'afficher les issues d'un projet directement
    dans l'interface admin du projet sous forme de tableau.

    Attributs :
        model (Model) : le modèle à utiliser pour cet inline (ici Issue)
        extra (int)   : nombre de lignes vides supplémentaires à afficher
                        par défaut (0 signifie aucune ligne vide)
    """

    model = Issue
    extra = 0  # Pas de lignes vides supplémentaires


# ---------------------------------------------------------------------
# Inline pour les commentaires
# ---------------------------------------------------------------------
class CommentInline(admin.TabularInline):
    """
    Classe permettant d'afficher les commentaires d'une issue directement
    dans l'interface admin de l'issue sous forme de tableau.

    Attributs :
        model (Model) : le modèle à utiliser pour cet inline (ici Comment)
        extra (int)   : nombre de lignes vides supplémentaires à afficher
                        par défaut (0 signifie aucune ligne vide)
    """

    model = Comment
    extra = 0  # Pas de lignes vides supplémentaires


# ---------------------------------------------------------------------
# Admin pour les issues
# ---------------------------------------------------------------------
class IssueAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des issues dans l'interface admin.

    Attributs :
        inlines (list)     : liste des inlines associés à ce modèle
                             (ici les commentaires pour chaque issue)
        list_display (tuple) : champs affichés dans la liste des issues
        list_filter (tuple)  : filtres disponibles dans la colonne de droite
    """

    inlines = [CommentInline]  # Affiche les commentaires directement dans l'issue
    list_display = ("title", "project", "author", "status", "priority", "created_time")
    list_filter = ("project", "status", "priority", "tag")  # Filtres disponibles pour affiner la liste


# ---------------------------------------------------------------------
# Admin pour les projets
# ---------------------------------------------------------------------
class ProjectAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage des projets dans l'interface admin.

    Attributs :
        inlines (list)      : liste des inlines associés à ce modèle
                              (ici les contributeurs et les issues)
        list_display (tuple) : champs affichés dans la liste des projets
        list_filter (tuple)  : filtres disponibles dans la colonne de droite
    """

    inlines = [ContributorInline, IssueInline]  # Affiche contributeurs et issues dans le projet
    list_display = ("title", "type", "author", "created_time")
    list_filter = ("type", "author")  # Filtres pour le type de projet et l'auteur


# ---------------------------------------------------------------------
# Enregistrement des modèles dans l'admin
# ---------------------------------------------------------------------
admin.site.register(Project, ProjectAdmin)  # Projet avec issues et contributeurs
admin.site.register(Issue, IssueAdmin)  # Issue avec commentaires
admin.site.register(Contributor)  # Contributeurs (standalone)
admin.site.register(Comment)  # Commentaires (standalone)
