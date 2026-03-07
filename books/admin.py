from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year','created_at')
    search_fields = ('title', 'author')
    list_filter = ('published_year',)

# Register your models here.
