from django.conf.urls import patterns, include, url
from chess import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chessfellows.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('chess.urls')),
    url(r'^', include('registration.backends.default.urls')),
)
