from django.db import transaction
from rest_framework import pagination, serializers

from books.models import Book
from users.serializers import CurrentUserSerializer

from .models import Profile


class RelationPaginator(pagination.PageNumberPagination):
    """For nested serializer pagination"""

    def get_paginated_response(self, data):
        return {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }


class ProfileBookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover_image"]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    def update(self, instance, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop("user")
            user = instance.user

            user_ser = CurrentUserSerializer(instance=user, data=user_data)
            if user_ser.is_valid():
                user_ser.save()

            return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "email",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "about",
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    This serializer is for displaying a user favorite books list
    """

    user = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    favorite_list = serializers.SerializerMethodField(read_only=True)

    def get_favorite_list(self, obj):
        # books = Book.objects.filter(favorite=obj.user.id)
        books = obj.user.favorite_books.all()
        serializer = ProfileBookSerializer(books, many=True)
        paginator = RelationPaginator()
        paginate_data = paginator.paginate_queryset(
            queryset=serializer.data, request=self.context["request"]
        )
        result = paginator.get_paginated_response(paginate_data)
        return result

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "email",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "about",
            "favorite_list",
        ]
