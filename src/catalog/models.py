from django.db import models
from django.urls import reverse # ==>  'reverse' is used to generate URLs by returning a url pattern that matches that instance
import uuid # ==> for generating  unique IDs

# Create your models here.
class Book(models.Model):
    """Model representation for a book """
    title = models.CharField(max_length=200)
    # Books have a Many-to-One relationship with Authors; Therefore a Foreign Key is required because Author can have multiple book
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text="13 Characters that Identifies a book")
    genre = models.ManyToManyField('Genre', help_text="Select a genre for this book")
    language = models.ManyToManyField('Language', help_text="Select a language for this book")
    image = models.URLField(null=True)


    def __str__(self):
        """This represents the Model Object"""
        return f"{self.title} ({self.author})"

    def get_absolute_url(self):
        """This returns a URL to access a book."""
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """ Model representation for a specific copy of a book"""
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this specific copy of the book across the whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m', help_text="Book Availability")

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    """Model respresenting an Author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Genre(models.Model):
    """ Models Representing a book genre"""
    name = models.CharField(max_length=100, help_text="Enter a book genre (e.g. Romance, Fiction)")

    def __str__(self):
        return self.name

class Language(models.Model):
    """Model representing a Language"""
    name = models.CharField(max_length=100, help_text="Enter a language name")

    def __str__(self):
        return self.name