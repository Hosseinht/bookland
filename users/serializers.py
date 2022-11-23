from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class DeleteUserSerializer(serializers.ModelSerializer):
    """
        Default serializer needs password for deletion. I override this because I don't
        want to put password for deleting a user
    """
    class Meta:
        model = User
        fields = ['id']


class UserCreateSerializer(BaseUserCreateSerializer):
    """
        Default implementation just have username, email and password. Here I want to show more field
        based on user
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["user"]
        if user == user.is_superuser or user.is_staff:
            self.Meta.fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "password",
                "is_active",
                "is_staff",
                "is_superuser",
            ]
        elif user.is_anonymous:
            self.Meta.fields = [
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "password",
            ]
