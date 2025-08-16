from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["author", "created_time"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = "__all__"

    def validate(self, data):
        # Empêcher qu'un user soit ajouté 2x au même projet
        if Contributor.objects.filter(user=data["user"], project=data["project"]).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur de ce projet.")
        return data


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["author", "created_time"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created_time"]
