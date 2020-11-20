from django.shortcuts import render
from catalog.models import Book

def index(request):
    """Veiw function for the Index page"""

    #numbers of Books
    num_books = Book.objects.all().count()

    #return the HTML template with context data
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books
        }
    )
