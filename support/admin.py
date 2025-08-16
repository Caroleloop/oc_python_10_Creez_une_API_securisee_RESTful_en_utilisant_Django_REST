from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


# Inline pour les contributeurs
class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 0  # pas de lignes vides supplémentaires


# Inline pour les issues
class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0


# Inline pour les commentaires (affiché dans les issues)
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


# Admin pour les issues avec commentaires
class IssueAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ("title", "project", "author", "status", "priority", "created_time")
    list_filter = ("project", "status", "priority", "tag")


# Admin pour les projets avec issues et contributeurs
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ContributorInline, IssueInline]
    list_display = ("title", "type", "author", "created_time")
    list_filter = ("type", "author")


# Enregistrement des modèles
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Contributor)
admin.site.register(Comment)
