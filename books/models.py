from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

from .managers import ReviewManager, BookManager
from .validators import validate_isbn


class Author(models.Model):
    name = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Book(models.Model):
    author = models.ManyToManyField(Author, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    pages = models.PositiveSmallIntegerField()
    isbn = models.CharField(max_length=13, validators=[validate_isbn(), MaxLengthValidator(13)])
    cover_image = models.ImageField(upload_to='books/images')
    publish = models.BooleanField(default=True)
    favorite = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favorite_books', blank=True)
    add_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

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
    add_date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = ReviewManager()

    def __str__(self):
        return f"{self.user.username} {self.book.title}"
