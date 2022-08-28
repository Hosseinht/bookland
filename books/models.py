from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models.aggregates import Avg

from .validators import validate_isbn


class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('reviews')


class ReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('user', 'book')


class Author(models.Model):
    name = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ManyToManyField(Author, related_name='books')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    pages = models.PositiveSmallIntegerField()
    isbn = models.CharField(max_length=13, validators=[validate_isbn(), MaxLengthValidator(13)])
    # isbn = models.DecimalField(max_digits=13, decimal_places=0)
    cover_image = models.ImageField(upload_to='books/images')
    publish = models.BooleanField(default=True)

    @property
    def average_rating(self):
        avg_rating = Review.objects.select_related('book').filter(book_id=self.id).aggregate(Avg('rating'))

        return str(avg_rating['rating__avg'])

    objects = BookManager()

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING, default=5)
    date_added = models.DateField(auto_now_add=True)

    objects = ReviewManager()

    @property
    def average_rating(self):
        return Review.objects.filter(book_id=self.book.id).aggregate(
            average_rating=Avg('rating'))


    def __str__(self):
        return f"{self.user.username} {self.book.title}"
