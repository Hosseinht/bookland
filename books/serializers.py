from django.db.models import Avg, Subquery, Count
from rest_framework import serializers
from rest_framework.fields import IntegerField

from .models import Author, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym"]


class ReviewFixedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['average_rating']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField(read_only=True)
    book = serializers.SlugRelatedField(slug_field='title', read_only=True)

    def get_reviewer(self, review: Review):
        return review.user.username

    def create(self, validated_data):
        book_id = self.context['book_id']
        user = self.context['user']

        if Review.objects.filter(book_id=book_id, user=user):
            raise serializers.ValidationError('You have already reviewed')
        return Review.objects.create(book_id=book_id, user=user, **validated_data)

    class Meta:
        model = Review
        fields = [
            "id",
            "book",
            "reviewer",
            "description",
            'rating',
        ]


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    isbn = serializers.IntegerField()
    # author = AuthorSerializer(many=True)
    author = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Author.objects.all())

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
            'average_rating',
        ]

    # read_only_fields = ('average_rating',)


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    isbn = serializers.IntegerField()

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
            'reviews',
        ]
