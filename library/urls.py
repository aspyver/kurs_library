from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^$', views.areas_of_expertises, name='areas_of_expertises'),
    url(r'^categories/$', views.areas_of_expertises, name = "areas_of_expertises"),
    url(r'^category/((?P<area_id>\d+)/)?$', views.area_of_expertise, name = "area_of_expertise"),
    url(r'^books/((?P<book_id>\d+)/)?$', views.book, name = "book"),
    #url(r'^search-cat/$', views.search_area_form, name = "search_category"),
    url(r'^search/$', views.search, name="search"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
