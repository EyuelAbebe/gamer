from django.conf.urls import patterns, url
from django.contrib import admin
from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home', views.home_page, name='home'),
    url(r'^history$', views.history_page, name='history'),
    url(r'^profile$', views.profile_page, name='profile'),
)


