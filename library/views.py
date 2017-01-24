from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from library.models import AreaOfExpertise, Book, Reader, ReaderBookCard, BookCopy
from django.db import connection, models
from library.forms import LoginForm
from django.contrib.auth import login, logout
from datetime import date, timedelta
from django.utils import timezone
from django.core.exceptions import PermissionDenied

'''
from django.views.generic import ListView
from django.db.models import Q
'''
def index(request):
    return HttpResponse("Hello, my friend.  You're at the library index. Let's try this ugly composition of shit!")


#Стартовая страница. Отображения списка областей знаний в меню
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


#Отображение книг по заданной области знаний
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
		'areas': AreaOfExpertise.objects.all().order_by("area_name"),
		'area': ar,
		'books': books,
	})
	
	
#Отображение информации для заданной книги
def book(request, book_id):
	if book_id == None:
		book = Book.objects.first()
	else:
		try:
			book = Book.objects.get(pk=book_id)
		except Book.DoesNotExist:
			raise Http404
	#authors = Book.objects.filter(books=book_id)[:4]
	return render(request, 'book.html', {
	    'areas': AreaOfExpertise.objects.all().order_by("area_name"),
	    'book': book,
	    'authors': book.authors.all()[:4],
	    'book_areas': book.areas.all(),
	})

	
	
#Высчитывание кол-ва экземпляров книги в библиотеке (PostgreSQL)	
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

'''
def search_area_form(request):
    return render_to_response('search_area_form.html')
'''	


#Осуществление поиска по областям знаний
def search(request):
    if 'q' in request.GET:
        #message = 'You searched for: %r' % request.GET['q']
        q = request.GET['q']
        areas = AreaOfExpertise.objects.filter(area_name__icontains=q)
        return render_to_response('search_results.html', {
		    's_areas': areas, 
		    'query': q,
		    'areas': AreaOfExpertise.objects.all().order_by("area_name"),
		})
    else:
        #message = 'You submitted an empty form.'
        #return HttpResponse('Please submit a search term.')
        return render(request, 'categories.html', {
			'areas': AreaOfExpertise.objects.all().order_by("area_name"),
		})
    #return HttpResponse(message)
    
    
#Вход в систему для работников    	
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/library/staff/')
    form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'areas': AreaOfExpertise.objects.all().order_by("area_name"),
    })		


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/library/')
	
	
def staff(request):
	if request.user.is_authenticated():
		return render(request, 'staff_s-page.html' )
	else:
		return HttpResponseRedirect('/library/')
		
		
def librarian(request):
	if request.user.is_authenticated():
		#проверка, что это сотрудник абнонемента или чительного зала
		return render(request, 'librarian_s-page.html' )
	else:
		return HttpResponseRedirect('/library/')
		
		
def readers_list(request):
	if request.user.is_authenticated():
		
		return render(request, 'readers.html', {
		    'readers': Reader.objects.all().order_by("surname", "name"),
		})
	else:
		return HttpResponseRedirect('/library/')
		
def reader(request, reader_id):
	if request.user.is_authenticated():
		if reader_id == None:
			reader = Reader.objects.first()
		else:
			try:
				reader = Reader.objects.get(pk=reader_id)
			except Book.DoesNotExist:
				raise Http404

		#cbooks=ReaderBookCard.objects.filter(readers=reader_id, return_date=None)
		bookcards=ReaderBookCard.objects.filter(readers=reader_id).order_by("taken_date")
		'''
		s = "Книги: <br><br>"
		for bookcard in bookcards:
			s = s + "(" + str(bookcard.pk) + str(bookcard.taken_date)+ ") "+"<br>"
		return HttpResponse(s)
		'''
		return render(request, 'reader.html', {
		    'reader': reader,
		    'bookcards': bookcards,
		})
		
		
	else:
		return HttpResponseRedirect('/library/')		
		
		
def return_book(request):
	if request.user.is_authenticated():
		if 'bookcard_id' in request.GET:
			bookcard_id = request.GET['bookcard_id']
			book = ReaderBookCard.objects.get(pk=bookcard_id)
			#book.return_date = date.now()
			book.return_date = timezone.now()
			book.save()		
		if 'reader_id' in request.GET:
			reader_id = request.GET['reader_id']
		else:
			reader_id = 1
		return HttpResponseRedirect('/library/s/reader/' + str(reader_id) + '/')
		
	else:
		return HttpResponseRedirect('/library/')			
		
		
def get_book(request):
	if request.user.is_authenticated():
		if 'bookcopy_id' in request.GET:
			bookcopy_id = request.GET['bookcopy_id']
			try: #does bookcopy exist
				bookcopy = BookCopy.objects.get(pk=bookcopy_id)
			except BookCopy.DoesNotExist:
				raise Http404
			#does bookcopy in library
			if ReaderBookCard.objects.filter(bookcopy_number=bookcopy_id, return_date=None):
				return HttpResponse('Книга уже кому-то выдана')
			else:
				bookcard = ReaderBookCard(bookcopy_number=bookcopy, taken_date=timezone.now(), employee_give=request.user)
				if 'reader_id' in request.GET:
					reader_id = request.GET['reader_id']
					try: #does reader exist
						reader = Reader.objects.get(pk=reader_id)
					except Reader.DoesNotExist:
						raise Http404
					bookcard.save()	
					reader.reader_books.add(bookcard)
				else:
					return HttpResponse('No reader')
				return HttpResponseRedirect('/library/s/reader/' + str(reader_id) + '/')
		else:
			return HttpResponseRedirect('/library/s/readers')
		
	else:
		return HttpResponseRedirect('/library/')		





		
'''
class AreaSearchForm(ListView):
    model = AreaOfExpertise

    def get_queryset(self):
        # Получаем не отфильтрованный кверисет всех моделей
        queryset = super(ListView, self).get_queryset()
        q = self.request.GET.get("q")
        if q:
        # Если 'q' в GET запросе, фильтруем кверисет по данным из 'q'
            return queryset.filter(Q(area_name__icontains=q))
        return queryset
'''
