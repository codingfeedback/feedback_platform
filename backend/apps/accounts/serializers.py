from rest_framework import serializers

from .models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "public_handle", "gender", "country_code", "age_group", "bio")
        read_only_fields = fields


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "public_handle",
            "auth_provider",
            "provider_subject",
            "gender",
            "country_code",
            "age_group",
            "bio",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
