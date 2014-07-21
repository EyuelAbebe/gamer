from django.conf.urls import patterns, include, url

from django.contrib import admin

from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.base, name='base'),
    url(r'^player(?P<player_id>\d+)/$', views.profile, name='profile'),
    url(r'^matchmaking/player(?P<player_id>\d+)/$',
        views.match_making, name='match_making'),
    url(r'^m(?P<match_id>\d+)/w(?P<wht_id>\d+)/b(?P<blk_id>\d+)/$',
        views.match, name='match'),
    url(r'^gameover/w(?P<win_id>\d+)/l(?P<lose_id>\d+)/$',
        views.match_result, name='match_result'),
)
