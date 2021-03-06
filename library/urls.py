from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^$', views.areas_of_expertises, name='areas_of_expertises'),
    url(r'^categories/$', views.areas_of_expertises, name = "areas_of_expertises"),
    url(r'^category/((?P<area_id>\d+)/)?$', views.area_of_expertise, name = "area_of_expertise"),
    url(r'^books/((?P<book_id>\d+)/)?$', views.book, name = "book"),
    url(r'^search/$', views.search, name="search"),
    url(r'^login/$', views.user_login, name='login'),
    
    url(r'^logout/.*$', views.user_logout, name='new'),
    url(r'^staff/$', views.staff, name='staff_start-page'),
    
    url(r'^s/lib/$', views.librarian, name='librarian_start-page'),
    url(r'^s/readers/$', views.readers_list, name = "readers"),
    url(r'^s/reader/((?P<reader_id>\d+)/)?$', views.reader, name = "reader"),
    url(r'^s/return/$', views.return_book, name = "return_book"),
    url(r'^s/get/$', views.get_book, name = "get_book"),
    url(r'^s/bad_readers/$', views.bad_readers_list, name = "bad_readers_list"),
    url(r'^s/statistics/$', views.statistics, name = "statistics"),
    
    url(r'^s/man/$', views.manager, name='manager_start-page'),
    url(r'^s/add-books/$', views.add_books, name='add_books'),
    url(r'^s/add-bookcopies/$', views.add_bookcopies, name='add_bookcopies'),
    url(r'^s/del-book/$', views.del_book_list, name='del_book-list'),
    url(r'^s/del-book/copies/((?P<book_id>\d+)/)?$', views.del_bookcopies_list, name='del_bookcopies'),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
