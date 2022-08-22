from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet


from .models import Author, Book, Review
from .serializers import AuthorSerializer, BookSerializer, ReviewSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
