from django.urls import path
from .views import index, BookDetailView
#catalog
#catlog/books/
#catalog/authors
#catolog/book/<id: e.g 3>

urlpatterns = [
    path('', index, name="index"),
    path('book/<int:pk>', BookDetailView.as_view(), name="book-detail")  
]