from django.contrib import admin

from .models import Book, Author, Genre, Language, BookInstance

#Register Models
admin.site.register(Book)

#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(BookInstance)

