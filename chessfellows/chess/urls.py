from django.conf.urls import patterns, url
from django.contrib import admin
from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/home/', views.home_page, name='home'),
    url(r'^accounts/history/$', views.history_page, name='history'),
    url(r'^accounts/profile/$', views.profile_page, name='profile'),
    url(r'^$', views.base, name='base'),
)


