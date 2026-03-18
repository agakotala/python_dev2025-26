from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Book
from .forms import BookForm, RegisterForm
from .serializers import BookSerializer


@login_required
def book_list(request):
    # Pobieramy tekst wyszukiwania z adresu URL, np. ?q=lem
    query = request.GET.get("q", "")

    # Pobieramy sposób sortowania z adresu URL.
    # Domyślnie ustawiamy "newest", żeby najnowsze książki były na górze.
    sort = request.GET.get("sort", "newest")

    # Bardzo ważne: pokazujemy tylko książki zalogowanego użytkownika.
    # Dzięki temu jeden użytkownik nie widzi danych drugiego.
    books = Book.objects.filter(owner=request.user)

    # Jeśli użytkownik coś wpisał w wyszukiwarkę,
    # to filtrujemy po tytule LUB autorze.
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )

    # Sortowanie - pozwala uporządkować wyniki na różne sposoby.
    if sort == "title_asc":
        books = books.order_by("title")
    elif sort == "title_desc":
        books = books.order_by("-title")
    elif sort == "year_asc":
        books = books.order_by("published_year")
    elif sort == "year_desc":
        books = books.order_by("-published_year")
    elif sort == "oldest":
        books = books.order_by("created_at")
    else:
        books = books.order_by("-created_at")

    return render(
        request,
        "books/book_list.html",
        {
            "books": books,
            "query": query,
            "sort": sort,
        },
    )


@login_required
def book_detail(request, pk):
    # Poprawka bezpieczeństwa:
    # pobieramy książkę nie tylko po pk, ale też po owner=request.user.
    # Dzięki temu użytkownik nie podejrzy cudzej książki po ręcznej zmianie URL-a.
    book = get_object_or_404(Book, pk=pk, owner=request.user)

    return render(
        request,
        "books/book_detail.html",
        {
            "book": book,
        }
    )


@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)

        if form.is_valid():
            # commit=False oznacza:
            # "utwórz obiekt w pamięci, ale jeszcze nie zapisuj do bazy"
            # Dzięki temu możemy dopisać właściciela.
            book = form.save(commit=False)

            # Każda książka ma być przypisana do zalogowanego użytkownika.
            book.owner = request.user
            book.save()

            messages.success(request, "Książka została dodana.")
            return redirect("book_list")
    else:
        form = BookForm()

    return render(
        request,
        "books/book_form.html",
        {
            "form": form,
            "title": "Dodaj książkę",
        },
    )


@login_required
def book_update(request, pk):
    # Znów zabezpieczenie: użytkownik może edytować tylko swoją książkę.
    book = get_object_or_404(Book, pk=pk, owner=request.user)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            form.save()
            messages.success(request, "Książka została zaktualizowana.")
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "books/book_form.html",
        {
            "form": form,
            "title": "Edytuj książkę",
        }
    )


@login_required
def book_delete(request, pk):
    # Usuwamy tylko własne rekordy.
    book = get_object_or_404(Book, pk=pk, owner=request.user)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Książka została usunięta.")
        return redirect("book_list")

    return render(request, "books/book_confirm_delete.html", {"book": book})


def register_view(request):
    # Jeśli formularz rejestracji został wysłany
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Po rejestracji od razu logujemy użytkownika,
            # żeby nie musiał logować się drugi raz ręcznie.
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()

    return render(
        request,
        "books/register.html",
        {
            "form": form,
        }
    )


def login_view(request):
    if request.method == "POST":
        # AuthenticationForm to gotowy formularz Django do logowania.
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("book_list")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "books/login.html",
        {
            "form": form,
        }
    )


def logout_view(request):
    # Wylogowujemy użytkownika i wracamy na stronę logowania.
    logout(request)
    return redirect("login")


class BookListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    # Tylko zalogowany użytkownik może używać API.
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # API ma zwracać wyłącznie książki bieżącego użytkownika.
        return Book.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Gdy książka jest tworzona przez API,
        # właściciel ma być ustawiony automatycznie.
        serializer.save(owner=self.request.user)


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # To samo zabezpieczenie dla podglądu / edycji / usuwania przez API.
        return Book.objects.filter(owner=self.request.user)