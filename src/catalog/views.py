from django.shortcuts import render
from catalog.models import Book
from django.views import generic

def index(request):
    """Veiw function for the Index page"""

    #numbers of Books
    num_books = Book.objects.all().count()
    all_books = Book.objects.all().order_by("-id")

    #return the HTML template with context data
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'books': all_books
        }
    )


class BookDetailView(generic.DetailView):
    model = Book