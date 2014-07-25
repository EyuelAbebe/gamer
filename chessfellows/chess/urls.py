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
    url(r'^accounts/join_table/(?P<match_id>\d+)/$', views.join_table, name='join_table'),
    url(r'^accounts/signUp/$', views.signUp, name='signup'),
    url(r'^/register/$', views.signUp, name='signup'),
    url(r'^updateUserInfo/$', views.update_user, name='update_ui'),
    url(r'^updatePlayerInfo/$', views.update_player, name='update_pi'),
    url(r'^my_login/', views.Login, name='login'),
    url(r'^$', views.landing, name='landing'),
    url(r'^game/move/$', views.make_move, name='make_move'),
    url(r'^read_match/$', views.join_table_moves, name='join_table_moves')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


