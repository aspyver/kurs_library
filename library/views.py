from django.shortcuts import render
from django.http import HttpResponse, Http404
from library.models import AreaOfExpertise, Book

def index(request):
    return HttpResponse("Hello, my friend.  You're at the library index. Let's try this ugly composition of shit!")


def areas_of_expertises(request):
	areas = AreaOfExpertise.objects.all().order_by("area_name")
	s = "Области знаний: <br><br>"
	for area in areas:
		s = s + "(" + str(area.pk) + ") " + area.area_name + "<br>"
	#return HttpResponse(s)
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
	s = "Область знаний: " + ar.area_name + "<br><br>"
	for book in books:
		s = s + "(" + str(book.pk) + ") " + book.book_name + "<br>"
	#return HttpResponse(s)
	return render(request, 'books.html', {
		'area': area_id,
		'books': books,
	})
