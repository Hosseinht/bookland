from django.db import models


class ReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user', 'book')


class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related("author")
