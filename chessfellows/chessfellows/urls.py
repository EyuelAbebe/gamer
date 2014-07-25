from django.conf.urls import patterns, include, url
from chess import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'updatePlayerInfo/', views.update_player, name='update_pi'),
    url(r'', include('chess.urls')),
    url(r'', include('registration.backends.default.urls')),
    url(r'^chat/', include('chatrooms.urls')),
    url(r'^', include('registration.backends.default.urls')),
)

urlpatterns += staticfiles_urlpatterns()
