from django.contrib import admin

from .models import Book, Author, Genre, Language, BookInstance

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book","status", "due_back")
    list_filter = ("status", "due_back")

    # Field set is used for categorising/grouping set of properties in a model Object
    fieldsets = (
        ("Book Details", {
            'fields': ("book", "id")
        }),
        ("Availability", {
            "fields": ("status", "due_back")
        })
    )

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def get_genre(self, object):
        return ",".join([genre.name for genre in object.genre.all()])
    
    list_display = ("title", "author", "get_genre")
    inlines = [BooksInstanceInline]


#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", "image", "bio", ("date_of_birth", "date_of_death")]
    search_fields = ["last_name"]

    inlines = [BookInline]


admin.site.register(Genre)
admin.site.register(Language)


