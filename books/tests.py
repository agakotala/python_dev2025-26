from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookModelTest(TestCase):
    def setUp(self):
        # Tworzymy użytkownika potrzebnego do owner
        self.user = User.objects.create_user(
            username="ania",
            password="Test12345!"
        )

    def test_book_str(self):
        # owner jest wymagany przez aktualny model,
        # więc musimy go podać w teście
        book = Book.objects.create(
            owner=self.user,
            title="Wiedźmin",
            author="Andrzej Sapkowski",
            published_year=1993,
            genre="fantasy",
            description="Fantastyka"
        )

        self.assertEqual(str(book), "Wiedźmin - Andrzej Sapkowski")


class BookViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ania",
            password="Test12345!"
        )

        self.other_user = User.objects.create_user(
            username="ola",
            password="Test12345!"
        )

        self.book = Book.objects.create(
            owner=self.user,
            title="Solaris",
            author="Stanisław Lem",
            published_year=1961,
            genre="science fiction",
            description="Klasyka SF"
        )

    def test_book_list_requires_login(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_sees_own_book(self):
        self.client.login(username="ania", password="Test12345!")
        response = self.client.get(reverse("book_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Solaris")

    def test_user_cannot_open_other_user_book(self):
        other_book = Book.objects.create(
            owner=self.other_user,
            title="Obca książka",
            author="Ktoś",
            published_year=2020,
            genre="dramat",
            description="Nie powinna być widoczna"
        )

        self.client.login(username="ania", password="Test12345!")
        response = self.client.get(reverse("book_detail", args=[other_book.pk]))

        # Po naszej poprawce ma być 404, bo to nie jest książka Ani
        self.assertEqual(response.status_code, 404)

    def test_book_create(self):
        self.client.login(username="ania", password="Test12345!")

        response = self.client.post(
            reverse("book_create"),
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "published_year": 1965,
                "genre": "science fiction",
                "description": "Klasyka",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title="Dune", owner=self.user).exists())