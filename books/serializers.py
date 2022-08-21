from rest_framework import serializers

from .models import Author, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym"]


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "title",
            "description",
            "price",
            "publisher",
            "language",
            "pages",
            "isbn",
            'publish',
            "cover_image",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "book", "user", "description", "date_added"]
