from django.contrib import admin
from library.models import AreaOfExpertise, Author, Book, BookCopy, ReaderBookCard, Reader

admin.site.register(AreaOfExpertise)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(ReaderBookCard)
admin.site.register(Reader)

# Register your models here.
