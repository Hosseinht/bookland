from django_filters.rest_framework import FilterSet
from .models import Book


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'language': ['iexact'],
            'author__name': ['iexact'],
            'price': ['exact'],
        }
