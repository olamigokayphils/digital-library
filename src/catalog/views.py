from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookInstance, Author
from django.views import generic
from django.http import Http404

def index(request):
    """Veiw function for the Index page"""

    #numbers of Books
    num_books = Book.objects.all().count()
    all_books = Book.objects.all().order_by("-id")

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    #return the HTML template with context data
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'books': all_books,
            "num_visits": num_visits
        }
    )


# class BookDetailView(generic.DetailView):
#     model = Book

def book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book request cannot be found")
    
    # CHECK IF BOOK IS AVAILABLE FOR RENT
    copies_available = BookInstance.objects.filter(book=book, status="a").count()


    return render(
        request,
        "catalog/book_detail.html",
        context= {
            'book': book,
            'copies': copies_available
        }
    )


def author_list_view(request):
    authors = Author.objects.all().order_by("first_name")

    return render(
        request,
        "catalog/authors_list.html",
        context={
            "authors": authors,
            "numbers_of_authors": authors.count()
        }
    )

def author_detail_view(request, pk, slug):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)

    return render(
        request,
        "catalog/author_detail.html",
        context={
            "author": author,
            "books": books
        }
    )
