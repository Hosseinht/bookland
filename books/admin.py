from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Author, Book, Review


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "authors",
        "price"
    ]
    list_display_links = ["id", "title"]

    def authors(self, obj):
        return ", ".join([a.name for a in obj.author.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "book",
        "rating",

    ]
    list_display_links = ["id", "book"]


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
