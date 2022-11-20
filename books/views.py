from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from .filters import BookFilter
from .models import Author, Book, Review, Category
from .permissions import IsReviewUserOrReadOnly, IsAdminUserOrReadOnly
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    BookSerializer,
    ReviewSerializer,
    CategorySerializer,
)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "pseudonym"]
    ordering_fields = ["name"]

    def get_serializer_context(self):
        return {"author_id": self.kwargs.get("pk"), "request": self.request}

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        else:
            return AuthorDetailSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {"category_id": self.kwargs.get("pk")}


class BookViewSet(ModelViewSet):
    queryset = Book.objects.annotate(average_rating=Avg("reviews__rating")).order_by('-add_date')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ["title", "description"]
    ordering_fields = ["name", "price", "pages"]
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_context(self):

        return {"book_id": self.kwargs.get("pk"), "request": self.request}

    def get_serializer_class(self):
        if self.action == "list":
            return BookSerializer
        elif self.action == "create":
            return BookCreateSerializer

        else:
            return BookDetailSerializer

    @action(detail=True, methods=["put", "get"], permission_classes=[IsAuthenticated])
    def add_to_favorite(self, request, pk):
        """
        Add a book to a user's favorite list. actually add a user to the favorite field in Book model
        The endpoint will be:
        http://127.0.0.1:8000/api/books/1/add_to_favorite/
        By hitting this endpoint user will be added to the favorite field in Book model
        """
        bad_request_message = "An error has occurred"

        book = get_object_or_404(Book, pk=pk)
        user = self.request.user
        if user.is_authenticated and user not in book.favorite.all():
            book.favorite.add(user)
            return Response(
                {"detail": "Added to favorite list"}, status=status.HTTP_200_OK
            )
        elif user.is_authenticated and user in book.favorite.all():
            book.favorite.remove(user)
            return Response(
                {"detail": "Removed from favorite list"}, status=status.HTTP_200_OK
            )
        else:
            Response(
                {"detail": bad_request_message}, status=status.HTTP_400_BAD_REQUEST
            )


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewUserOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_pk"])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        avg = queryset.aggregate(average_rating=Avg("rating"))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(
                {"average_rating": avg["average_rating"], "item": serializer.data}
            )
        else:
            serializer = ReviewSerializer(queryset, many=True)
            return Response(
                {"average_rating": avg["average_rating"], "item": serializer.data}
            )

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"], "user": self.request.user}


# class BookFavoriteViewSet(APIView):
#       """
#           another approach to add a book to favorite list
#           urlpatterns = [
#                   path('books/<int:pk>/favorite/', views.BookFavoriteViewSet.as_view()),
#               ]
#       """
#
#     bad_request_message = 'An error has occurred'
#
#     def post(self, request, pk):
#         book = get_object_or_404(Book, pk=pk)
#         user = request.user
#         if user not in book.favorite.all():
#             book.favorite.add(user)
#             return Response({'detail': 'Added to favorite list'}, status=status.HTTP_200_OK)
#         elif user in book.favorite.all():
#             book.favorite.remove(user)
#             return Response({'detail': 'Removed from favorite list'}, status=status.HTTP_200_OK)
#         else:
#             Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)
