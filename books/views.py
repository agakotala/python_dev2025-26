from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm
from rest_framework import generics
from .serializers import BookSerializer

def book_list(request):
    query = request.GET.get("q", "")
    books = Book.objects.all().order_by("-created_at")

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    return render(request, "books/book_list.html", {"books": books, "query": query})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "books/book_detail.html", {"book": book})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "books/book_form.html", {"form": form, "title": "Dodaj książkę"})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {"form": form, "title": "Edytuj książkę"})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "books/book_confirm_delete.html", {"book": book})

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Create your views here.
