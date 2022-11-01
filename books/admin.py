from django.contrib import admin

from .models import Author, Book, Review, Category


class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "pseudonym",
    ]
    search_fields = ['name__istartswith', 'pseudonym__istartswith']


class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "authors",
        "price"
    ]
    list_display_links = ["id", "title"]
    autocomplete_fields = ['author']

    def authors(self, obj):
        return ", ".join([a.name for a in obj.author.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "book",
        "rating",

    ]
    list_display_links = ["id", "book"]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)
