from rest_framework import serializers

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
    reviewer = serializers.SerializerMethodField(read_only=True)
    book = serializers.SlugRelatedField(slug_field="title", read_only=True)

    def get_reviewer(self, review: Review):
        return review.user.username

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

        # read_only_fields = fields


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


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    def get_books(self, obj):
        author_pk = self.context["author_id"]
        books = Book.objects.select_related('category').filter(author=author_pk)

        return BookAuthorSerializer(books, many=True).data

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
    reviews = ReviewSerializer(many=True, read_only=True)
    isbn = serializers.IntegerField()
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
            "description",
            "price",
            "publisher",
            "language",
            "pages",
            "isbn",
            "cover_image",
            "reviews",
        ]
