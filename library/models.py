from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes

#blank=False, null=False - по умолчанию

class AreaOfExpertise (models.Model):
    area_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.area_name


class Author (models.Model):
    author_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.author_name

class Book (models.Model):
    isbn = models.CharField(max_length=32, unique=True)
    book_name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, db_table="libary_mm_bookhasauthor", related_name="books")
    book_city = models.CharField(max_length=64)
    publisher = models.CharField(max_length=64)
    pages_count = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    areas = models.ManyToManyField(AreaOfExpertise, db_table="library_mm_bookhasarea", related_name="books")

    def __str__(self):
        #return force_bytes('%s %s ' % (self.book_name, self.isbn)) + ', '.join([str(author.author_name)] for author in self.authors.all())
        return force_bytes('%s -- %s -- %s' % (self.book_name, self.isbn, self.publisher)) 
     
    def in_stock(self):
        self.objects.raw('''SELECT COUNT(*) FROM library_book AS book INNER JOIN library_bookcopy AS bc1
                            ON bc1.book_info_id = book.id
                            WHERE NOT EXISTS (
                            SELECT rbc.bookcopy_number_id FROM library_readerbookcard AS rbc INNER JOIN library_bookcopy AS bc2
                            ON rbc.bookcopy_number_id = bc2.id
                            WHERE ((rbc.taken_date = (
                            SELECT MAX(rbc.taken_date) FROM library_readerbookcard AS rbc INNER JOIN library_bookcopy AS bc3
                            ON rbc.bookcopy_number_id = bc3.id
                            WHERE bc2.id = bc3.id
                            )) AND (rbc.return_date IS NULL) AND (bc1.id = bc2.id)))
                            GROUP BY bc1.id''')

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

    def __str__(self):
        return force_bytes('%s on shelf %s, on rack %s' % (self.book_info.book_name.get(), str[self.shelf_number], str[self.rack_number]))


class ReaderBookCard (models.Model):
    bookcopy_number = models.ForeignKey(BookCopy, related_name="bookcopyincard", on_delete=models.CASCADE) #нужно ли related_name?
    taken_date = models.DateField(auto_now_add=True, blank=False)
    return_date = models.DateField(blank=True, null=True, default=models.SET_NULL) 
    employee_give = models.ForeignKey(User, related_name="books_given", blank=True, null=True, default=models.SET_NULL, on_delete=models.SET_NULL)
    employee_take = models.ForeignKey(User, related_name="books_taken", blank=True, null=True, default=models.SET_NULL, on_delete=models.SET_NULL) #как-то прописать сотрудника

    def __str__(self):
        return force_bytes('№ %d (%s), given on %s by %s. Returned on %s to %s' % (self.number.pk, str(self.taken_date), str(self.employee_give.username), str(self.return_date), str(self.employee_take.username)))

class Reader (models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    reader_books = models.ManyToManyField(ReaderBookCard, db_table="library_mm_readerhasbook", related_name="readers") 
    phone = models.CharField(max_length=32, default="-")

    def __str__(self):
        return force_bytes('%s %s, %s, %s' % (self.surname, self.name, self.address, self.phone))
