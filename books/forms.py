from django.utils import timezone
from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_year", "genre", "description"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control",
                                            "placeholder": "Wpisz tytuł książki",}),
            "author": forms.TextInput(attrs={"class": "form-control",
                                             "placeholder": "Wpisz autora",}),
            "published_year": forms.TextInput(attrs={"class": "form-control",
                                                     "placeholder": "Wpisz rok publikacji np.2024",}),
            "genre": forms.TextInput(attrs={"class": "form-control",
                                             "placeholder": "Wpisz gatunek, np. kryminał, science fiction",}),
            "description": forms.Textarea(attrs={"class": "form-control",
                                                 "rows": 6,
                                                 "placeholder": "Dodaj opis książki"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title and len(title.strip()) < 2:
            raise forms.ValidationError("Tytuł musi mieć co najmniej 2 znaki.")
        return title

    def clean_published_year(self):
        year = self.cleaned_data.get("published_year")
        current_year = timezone.now().year
        if year is not None:
            if year < 1000:
                raise forms.ValidationError("Rok wydania nie może być mniejszy niż 1000.")
            if year > current_year:
                raise forms.ValidationError(f"Rok wydania nie może być większy niż aktualny rok {current_year}.")
        return year

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


