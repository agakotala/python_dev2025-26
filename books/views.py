from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from rest_framework import generics
from .serializers import BookSerializer
from django.contrib import messages

@login_required
def book_list(request):
    query = request.GET.get("q", "")
    sort = request.GET.get("sort", "newst")
    books = Book.objects.filter(owner=request.user)
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))
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
    book = get_object_or_404(Book, pk=pk)
    return render(
        request,
        "books/book_detail.html",{
            "book": book,
        }
    )

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
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
    book = get_object_or_404(Book, pk=pk, owner=request.user)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Książka została usunięta.")
        return redirect("book_list")

    return render(request, "books/book_confirm_delete.html", {"book": book})


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Create your views here.
