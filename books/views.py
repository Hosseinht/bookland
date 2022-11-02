from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import BookFilter
from .models import Author, Book, Review, Category
from .permissions import IsReviewUserOrReadOnly, IsAdminUserOrReadOnly
from .serializers import (AuthorListSerializer, AuthorDetailSerializer, BookCreateSerializer,
                          BookDetailSerializer, BookSerializer,
                          ReviewSerializer, CategorySerializer)


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "pseudonym"]
    ordering_fields = ["name"]

    def get_serializer_context(self):
        return {"author_id": self.kwargs.get('pk'), 'request': self.request}

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        else:
            return AuthorDetailSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {"category_id": self.kwargs.get('pk')}


class BookViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Book.objects.annotate(average_rating=Avg("reviews__rating"))
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ["title", "description"]
    ordering_fields = ["name", "price", "pages"]

    def get_serializer_context(self):
        return {"book_id": self.kwargs.get("pk"), 'request': self.request}

    def get_serializer_class(self):
        if self.action == "list":
            return BookSerializer
        elif self.action == "create":
            return BookCreateSerializer
        else:
            return BookDetailSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewUserOrReadOnly]


    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_pk"])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        avg = queryset.aggregate(average_rating=Avg('rating'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response({'average_rating': avg['average_rating'], 'item': serializer.data})
        else:
            serializer = ReviewSerializer(queryset, many=True)
            return Response({'average_rating': avg['average_rating'], 'item': serializer.data})

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"], "user": self.request.user}
