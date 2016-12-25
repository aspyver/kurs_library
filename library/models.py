from django.db import models
from django.contrib.auth.models import User

#blank=False, null=False - по умолчанию

class AreaOfExpertise (models.Model):
    area_name = models.CharField(max_length=64, unique=True)


class Author (models.Model):
    author_name = models.CharField(max_length=255, unique=True)


class Book (models.Model):
    isbn = models.CharField(max_length=32, unique=True)
    book_name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, db_table="libary_mm_bookhasauthor", related_name="books")
    book_city = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    pages_count = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    areas = models.ManyToManyField(AreaOfExpertise, db_table="library_mm_bookhasarea", related_name="books")


"""
validators=[validate_isbn]

from django.core.exceptions import ValidationError
import re
def validate_isbn(value):
    if not match(r"(\d*-\d*-\d*-\d*-\d*)|(\d*-\d*-\d*-\d*)", value):
        raise ValidationError(u'isbn is not correct')
"""


class BookCopy (models.Model):
    book_info = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="bookcopies")
    shelf_number = models.IntegerField()
    rack_number = models.IntegerField()


class ReaderBookCard (models.Model):
    bookcopy_number = models.ForeignKey(BookCopy, on_delete=models.CASCADE) #нужно ли related_name?
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, unique=True)
    taken_date = models.DateField(auto_now_add=True, blank=False)
    return_date = models.DateField(blank=True, null=True, default=models.SET_NULL) 
    employee_give = models.ForeignKey(User, related_name="books_given", blank=True, null=True, default=models.SET_NULL, on_delete=models.SET_NULL)
    employee_take = models.ForeignKey(User, related_name="books_taken", blank=True, null=True, default=models.SET_NULL, on_delete=models.SET_NULL) #как-то прописать сотрудника


class Reader (models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    reader_books = models.ManyToManyField(ReaderBookCard, db_table="library_mm_readerhasbook", related_name="readers") 


