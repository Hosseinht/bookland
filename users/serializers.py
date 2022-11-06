from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', "is_active",
                  "is_staff",
                  "is_superuser", ]


class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', ]

    def __init__(self, *args, **kwargs):
        """
            only admin can see "is_active","is_staff" and "is_superuser" fields
        """
        super(UserCreateSerializer, self).__init__(*args, **kwargs)
        user = self.context['user']
        if user == user.is_superuser or user.is_staff:
            self.Meta.fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', "is_active",
                                "is_staff",
                                "is_superuser", ]
        else:
            self.Meta.fields = self.Meta.fields
