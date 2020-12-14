from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from catalog.models import Book, BookInstance, Author, RentedBook
from django.views import generic
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required



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


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # SAVE USER DETAILS
            form.save()
            # SEND SUCCESS MESSAGE TO TEMPLATE
            messages.success(request, "Login to complete signup")
            return redirect(reverse_lazy("login"))

        else:
            return render(
                request,
                "registration/signup.html",
                {
                    'form': form,
                }
            )
    else:
        form = UserCreationForm()
        return render(
            request,
            "registration/signup.html",
            {
                'form': form
            }
        )

@login_required
def user_profile(request):
    user_rented_books = RentedBook.objects.filter(user=request.user)
    return render(
        request,
        "profile.html",
        context={
            "user": request.user,
            "rented_books": user_rented_books
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
    if request.method == "POST":
        search_input = request.POST.get("author", "Empty").lower()
        
        # Get Matching Authors
        authors = Author.objects.filter(Q(
            first_name__icontains=search_input
            ) | Q(last_name__icontains=search_input))

        return render(
            request,
            "catalog/authors_list.html",
            context = {
                "authors": authors,
                "numbers_of_authors": authors.count(),
                "search_item": search_input
            }
        )


    else:
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


@login_required
def rent_book(request, pk):
    user = request.user
    RentedBook().user_rentbook(user=user, book_id=pk)

    return redirect(reverse_lazy("user-profile"))
