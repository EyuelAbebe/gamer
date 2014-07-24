from django.conf.urls.static import static
from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib import admin
from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/home/', views.home_page, name='home'),
    url(r'^accounts/history/$', views.history_page, name='history'),
    url(r'^accounts/profile/$', views.profile_page, name='profile'),
    url(r'^accounts/start_table/$', views.start_table, name='start_table'),
    url(r'^accounts/signUp/$', views.signUp, name='signup'),
    url(r'^accounts/register/$', views.signUp, name='signup'),
    url(r'^accounts/updateUserInfo/$', views.update_user, name='update_ui'),
    url(r'^accounts/updatePlayerInfo/$', views.update_player, name='update_pi'),
    url(r'^$', views.landing, name='landing'),
    url(r'^game/move/$', views.make_move, name='make_move')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


