from django_filters.rest_framework import FilterSet
from .models import Book


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'author__name': ['iexact'],
            'language': ['iexact'],
            'price': ['exact'],
            'category': ['exact']
        }
