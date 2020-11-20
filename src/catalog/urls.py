from django.urls import path
from .views import index
#catalog
#catlog/books/
#catalog/authors
#catolog/book/<id: e.g 3>

urlpatterns = [
    path('', index, name="index")  
]