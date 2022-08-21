from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    publisher = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    pages = models.PositiveSmallIntegerField()
    isbn = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='books/images')
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.book.title}"
