from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^categories/$', views.areas_of_expertises, name = "areas_of_expertises"),
    url(r'^category/((?P<area_id>\d+)/)?$', views.area_of_expertise, name = "area_of_expertise"),
]
