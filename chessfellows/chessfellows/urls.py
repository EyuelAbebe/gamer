from django.conf.urls import patterns, include, url
from chess import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('chess.urls')),
    url(r'^chat/', include('chatrooms.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
