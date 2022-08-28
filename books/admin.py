from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Author, Book, Review


class BookAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Review)
