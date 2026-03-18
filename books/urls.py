from django.urls import path
from . import views

urlpatterns = [
    # Strona główna aplikacji
    path("", views.book_list, name="book_list"),

    # CRUD książek
    path("book/<int:pk>/", views.book_detail, name="book_detail"),
    path("book/new/", views.book_create, name="book_create"),
    path("book/<int:pk>/edit/", views.book_update, name="book_update"),
    path("book/<int:pk>/delete/", views.book_delete, name="book_delete"),

    # Logowanie / rejestracja / wylogowanie

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    # API
    path("api/books/", views.BookListCreateAPIView.as_view(), name="api_book_list"),
    path("api/books/<int:pk>/", views.BookRetrieveUpdateDestroyAPIView.as_view(), name="api_book_detail"),
]