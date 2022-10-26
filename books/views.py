from django.db.models import Avg, Count
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Author, Book, Review
from .permissions import IsReviewUserOrReadOnly
from .serializers import AuthorSerializer, BookSerializer, BookDetailSerializer, ReviewSerializer, ReviewFixedSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class BookViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Book.objects.prefetch_related('author').annotate(average_rating=Avg('reviews__rating'))

    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer
        else:
            return BookDetailSerializer
            # parser_classes = [MultiPartParser, FormParser]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewUserOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_pk'])

    def get_serializer_context(self):
        return {"book_id": self.kwargs['book_pk'], "user": self.request.user}
