from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .filters import BookFilter
from .models import Author, Book, Review
from .permissions import IsReviewUserOrReadOnly
from .serializers import AuthorSerializer, BookSerializer, BookDetailSerializer, ReviewSerializer, ReviewFixedSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'pseudonym']
    ordering_fields = ['name']


class BookViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Book.objects.prefetch_related('author').annotate(average_rating=Avg('reviews__rating'))
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description']
    ordering_fields = ['name', 'price', 'pages']

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
