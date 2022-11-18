from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer


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


class UserCreateSerializer(BaseUserCreateSerializer):

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
