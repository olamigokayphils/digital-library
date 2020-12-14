from django.urls import path
from .views import index, book_detail_view
from .views import author_list_view, author_detail_view
from .views import rent_book

#catalog
#catlog/books/
#catalog/authors
#catolog/book/<id: e.g 3>

urlpatterns = [
    path('', index, name="index"),
    path('book/<int:pk>', book_detail_view, name="book-detail"),
    path('authors', author_list_view, name="author-list"),
    path('author/<int:pk>/<slug:slug>', author_detail_view, name="author-detail"),

    path('rent-book/<int:pk>', rent_book, name="rent-book")
]