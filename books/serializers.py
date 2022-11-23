from rest_framework import serializers, pagination

from .models import Author, Book, Category, Review
from rest_framework.reverse import reverse


class RelationPaginator(pagination.PageNumberPagination):
    """For nested serializer pagination"""

    def get_paginated_response(self, data):
        return {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym"]


class AuthorBookSerializer(serializers.ModelSerializer):
    """
    This serializer is used in AuthorDetailSerializer for displaying author's books

    """

    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )

    # cover_image = serializers.SerializerMethodField()
    #
    # def get_cover_image(self,obj):
    #     request = self.context.get('request')
    #     print(request)
    #     str(request.build_absolute_uri(obj.cover_image.url))
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

        books = Book.objects.select_related("category").filter(author=author_pk)
        serializer = AuthorBookSerializer(books, many=True,context=self.context)
        paginator = RelationPaginator()
        paginated_data = paginator.paginate_queryset(
            queryset=serializer.data, request=self.context["request"]
        )

        result = paginator.get_paginated_response(paginated_data)

        return result

    class Meta:
        model = Author
        fields = ["id", "name", "pseudonym", "about", "books"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


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


class BookCreateSerializer(serializers.ModelSerializer):
    isbn = serializers.IntegerField()
    author = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        queryset=Author.objects.all(),
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


class SimpleReviewSerializer(serializers.ModelSerializer):
    """
    This serializer is used in BookDetailSerializer for the review part
    """

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
        reviews = Review.objects.select_related("book", "user").filter(book_id=book_id)
        serializer = SimpleReviewSerializer(reviews, many=True)
        paginator = RelationPaginator()
        paginated_data = paginator.paginate_queryset(
            queryset=serializer.data, request=self.context["request"]
        )

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
        read_only_fields = ["favorite"]

    def __init__(self, *args, **kwargs):
        """
        /api/books/1/add_to_favorite/ is the endpoint for adding a book to the favorite list.
        This logic here, hide all the fields at this endpoint.
        """
        super(BookDetailSerializer, self).__init__(*args, **kwargs)
        pk = self.context["book_id"]
        book_url = reverse("books-detail", kwargs={"pk": pk})

        if self.context["request"].get_full_path() == f"{book_url}add_to_favorite/":
            for field in self.fields:
                self.fields[field].read_only = True
