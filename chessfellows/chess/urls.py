from django.conf.urls import patterns, include, url

from django.contrib import admin

from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chessfellows.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.base, name='base')
)