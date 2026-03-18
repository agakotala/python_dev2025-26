from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display mówi, jakie kolumny mają być widoczne w panelu admina
    list_display = (
        "title",
        "author",
        "owner",          # dodajemy owner, bo to aplikacja wieloużytkownikowa
        "genre",          # dodajemy genre, żeby łatwiej zarządzać danymi
        "published_year",
        "created_at",
    )

    # search_fields mówi, po czym admin ma wyszukiwać
    search_fields = (
        "title",
        "author",
        "genre",
        "owner__username",  # pozwala wyszukiwać po loginie właściciela
    )

    # list_filter dodaje boczne filtry w panelu admina
    list_filter = (
        "genre",
        "published_year",
        "created_at",
    )