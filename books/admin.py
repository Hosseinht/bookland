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
    fieldsets = (
        (
            "Author",
            {
                "fields": (
                    "author",
                )
            },
        ),
        (
            "Category",
            {
                "fields": (
                    "category",
                )
            },
        ),
        (
            "Book Info",
            {
                "fields": (
                    "title",
                    "description",
                    "price",
                    "publisher",
                    "language",
                    "pages",
                    "isbn",
                    "cover_image",
                )
            },
        ),
        ("Dates", {"fields": ("add_date", "update")}),
    )
    list_display = [
        "id",
        "title",
        "authors",
        "category",
        "price",

    ]
    list_display_links = ["id", "title"]
    list_select_related = ['category']
    autocomplete_fields = ['author']
    readonly_fields = ['add_date','update']

    def get_queryset(self, request):
        queryset = super(BookAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('author')
        return queryset

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
