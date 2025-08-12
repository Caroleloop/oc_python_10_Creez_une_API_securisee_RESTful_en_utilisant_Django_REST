from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True)

    class Meta:
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
        # extra_kwargs = {"password": {"write_only": True}}

    def validate_age(self, value):
        if value <= 15:
            raise serializers.ValidationError("L'utilisateur doit avoir plus de 15 ans.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)  # hash du mot de passe
        user.save()
        return user
