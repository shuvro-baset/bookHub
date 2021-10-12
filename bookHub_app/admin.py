from django.contrib import admin

from .models import *


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_name', 'author_name', 'book_rating', 'uploaded_time']
