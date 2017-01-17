from django.shortcuts import render
from django.http import HttpResponse, Http404
from library.models import AreaOfExpertise, Book
from django.db import connection

def index(request):
    return HttpResponse("Hello, my friend.  You're at the library index. Let's try this ugly composition of shit!")


def areas_of_expertises(request):
	areas = AreaOfExpertise.objects.all().order_by("area_name")
	'''
	s = "Области знаний: <br><br>"
	for area in areas:
		s = s + "(" + str(area.pk) + ") " + area.area_name + "<br>"
	return HttpResponse(s)
	'''
	return render(request, 'categories.html', {
		'areas': areas
	})


def area_of_expertise(request, area_id):
	if area_id == None:
		ar = AreaOfExpertise.objects.first()
	else:
		try:
			ar = AreaOfExpertise.objects.get(pk=area_id)
		except AreaOfExpertise.DoesNotExist:
			raise Http404
	books = Book.objects.filter(areas = ar).order_by("book_name")
	for book in books:
		update_book_in_stock(book)

			
	'''
	s = "Область знаний: " + ar.area_name + "<br><br>"
	for book in books:
		s = s + "(" + str(book.pk) + ") " + book.book_name + "<br>"
	return HttpResponse(s)
	'''
	return render(request, 'books.html', {
		'area': area_id,
		'books': books,
	})


def update_book_in_stock(book):
	book_id = book.id
	cursor = connection.cursor()
	#count = Book.objects.raw
	cursor.execute("""SELECT COUNT(*) FROM library_book AS book INNER JOIN library_bookcopy AS bc1
                            ON bc1.book_info_id = book.id
                            WHERE (NOT EXISTS (
                            SELECT rbc.bookcopy_number_id FROM library_readerbookcard AS rbc INNER JOIN library_bookcopy AS bc2
                            ON rbc.bookcopy_number_id = bc2.id
                            WHERE ((rbc.taken_date = (
                            SELECT MAX(rbc.taken_date) FROM library_readerbookcard AS rbc INNER JOIN library_bookcopy AS bc3
                            ON rbc.bookcopy_number_id = bc3.id
                            WHERE bc2.id = bc3.id
                            )) AND (rbc.return_date IS NULL) AND (bc1.id = bc2.id)))
                            and book.id = %s);""", [book_id])
	a = cursor.fetchone()
	book.book_in_stock_count = a[0] #a is tuple
	book.save()
