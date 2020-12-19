from django.db import models
from django.urls import reverse # ==>  'reverse' is used to generate URLs by returning a url pattern that matches that instance
import uuid # ==> for generating  unique IDs
from django.contrib.auth.models import User
from .errors import BookDoesNotExist, BookNotAvailable
from .errors import UserRentalRecordConflictError
from django.utils import timezone
import json

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


class RentedBook(models.Model):
    """
    Model representation for rented books
    """
    RENT_BOOK_STATUS = (
        ('ru', 'Running'),
        ('re', 'Returned')
    )

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True)
    book_instance = models.ForeignKey(BookInstance, on_delete=models.PROTECT)
    status = models.CharField(max_length=2, choices=RENT_BOOK_STATUS)

    @classmethod
    def user_rentbook(cls, user, book_id):
        """
        This method calls updates a Book_instance model. From (Rent --> Return)
        """
        
        try:
            # GET BOOK
            book = Book.objects.get(id=book_id)
            
            # CHECK FOR AVAILBLE BOOK INSTANCES
            available_book_instances = BookInstance.objects.filter(book=book, status="a").order_by("-pk")

            if available_book_instances.count() > 0:
                # Available
                # Select the First
                book_instance = available_book_instances[0]
                
                # Update Book Instance to Loan
                book_instance.status = "o"
                # Due Back in a week (==> 7 days)
                book_instance.due_back = timezone.now() + timezone.timedelta(days=7)
                book_instance.save(update_fields=[
                    "status",
                    "due_back"
                ])

                # Create rented book
                rented_book =  cls.objects.create(status="ru", user=user, book=book, book_instance=book_instance)

                return rented_book

            else:
                raise BookNotAvailable(book_title=book.title, book_id=book_id)

        except Book.DoesNotExist:
            raise BookDoesNotExist(book_id=book_id)

    
    def user_return_book(self, user):
        if user != self.user:
            raise UserRentalRecordConflictError(book_instance=self.book_instance)

        else:
            # If Rented Book status is Running
            if self.status == "ru":
                # GET & UPDATE BOOK INSTANCE
                instance = BookInstance.objects.get(id=self.book_instance.id)
                # update 
                instance.status = "a" # Available
                instance.save(update_fields=["status"])

                # UPDATE USER RENTED BOOK PROFILE
                self.status = "re" # RETURNED
                self.save(update_fields=["status"])

            # GENERICALLY RETURN SUCCESS (If no error is encountered)
            return json.loads('{"status": "success"}')




    def __str__(self):
        return f"{self.book_instance}"

class Author(models.Model):
    """Model respresenting an Author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.URLField(null=True)
    bio = models.TextField(null=True)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id), f"{self.first_name.lower()}-{self.last_name.lower()}"])

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