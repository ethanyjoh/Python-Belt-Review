from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add_book),
    url(r'^books/(?P<book_id>\d+)$', views.show),
    url(r'^review/(?P<book_id>\d+)$', views.review),
    url(r'^users/(?P<user_id>\d+)$', views.show_user),

]
