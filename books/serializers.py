from rest_framework import serializers, pagination

from .models import Author, Book, Category, Review


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name"
        ]


class ReviewSerializer(serializers.ModelSerializer):
    # average_rating = serializers.FloatField()
    reviewer = serializers.SerializerMethodField(read_only=True)
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)

    def get_reviewer(self, review: Review):
        return str(review.user.username)

    def create(self, validated_data):
        book_id = self.context["book_id"]
        user = self.context["user"]

        if Review.objects.filter(book_id=book_id, user=user):
            raise serializers.ValidationError("You have already reviewed")
        return Review.objects.create(book_id=book_id, user=user, **validated_data)

    class Meta:
        model = Review
        fields = [
            "id",
            "book",
            "reviewer",
            "description",
            "rating",
            # "average_rating"
        ]


class SimpleReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SerializerMethodField(read_only=True)

    def get_reviewer(self, review: Review):
        return review.user.username

    class Meta:
        model = Review
        fields = [
            "reviewer",
            "description",
            "rating",
        ]


class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()

    # author = AuthorSerializer(many=True)
    author = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=Author.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "category",
            "title",
            "price",
            "language",
            "pages",
            "cover_image",
            "average_rating",
        ]

        read_only_fields = fields


class BookAuthorSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "category",
            "title",
            "price",
            "language",
            "pages",
            "cover_image",

        ]

        read_only_fields = fields


class RelationPaginator(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):
        author_pk = self.context["author_id"]
        books = Book.objects.select_related('category').filter(author=author_pk)
        serializer = BookAuthorSerializer(books, many=True)
        paginator = RelationPaginator()
        paginated_data = paginator.paginate_queryset(
            queryset=serializer.data, request=self.context['request'])

        result = paginator.get_paginated_response(paginated_data)

        return result

    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym", "about", "books"]


class BookCreateSerializer(serializers.ModelSerializer):
    isbn = serializers.IntegerField()
    author = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=Author.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "category",
            "title",
            "description",
            "price",
            "publisher",
            "language",
            "pages",
            "isbn",
            "publish",
            "cover_image",
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    isbn = serializers.IntegerField()
    author = serializers.SlugRelatedField(
        slug_field="name", many=True, queryset=Author.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    def get_reviews(self, obj):
        book_id = self.context["book_id"]
        reviews = Review.objects.select_related('book', 'user').filter(book_id=book_id)
        serializer = SimpleReviewSerializer(reviews, many=True)
        paginator = RelationPaginator()
        paginated_data = paginator.paginate_queryset(
            queryset=serializer.data, request=self.context['request'])

        result = paginator.get_paginated_response(paginated_data)

        return result

    class Meta:
        model = Book
        fields = [
            "id",
            "author",
            "category",
            "title",
            "description",
            "price",
            "publisher",
            "language",
            "pages",
            "isbn",
            "cover_image",
            "reviews",
        ]
