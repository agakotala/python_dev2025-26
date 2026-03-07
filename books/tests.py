from django.test import TestCase
from django.urls import reverse
from .models import Book

class BookModelTest(TestCase):
    def test_book_srt(self):
        book = Book.objects.create(
            title = "Wiedźmin",
            author = "Andrzej Sapkowski",
            published_year = 1993,
            description = "Fantastyka"
        )
        self.assertEqual(str(book), "Wiedźmin - Andrzej Sapkowski")

class BookViewsTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title = "Nawyki warte miliony. Jak nauczyć się zachowań przynoszących bogactwo",
            author = "Tracy Brian",
            published_year = 2021,
            description = "Psychologia"
        )
    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nawyki warte miliony. Jak nauczyć się zachowań przynoszących bogactwo")

    def test_book_detail_view(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tracy Brian")

    def test_book_create_view(self):
        response = self.client.get(reverse("book_create"), {
            "title": "Solaris",
            "author": "Stanisław Lem",
            "published_year": 1961,
            "description": "Science fiction"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="Solaris").exists())


# Create your tests here.
