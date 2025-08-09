from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_age(self, value):
        if value <= 15:
            raise serializers.ValidationError("L'utilisateur doit avoir plus de 15 ans.")
        return value
