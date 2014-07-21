from django.conf.urls import patterns, include, url

from django.contrib import admin

from chess import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chessfellows.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.base, name='base'),
    url(r'^m_(?P<match_id>\d+)/w_(?P<wht_id>\d+)/b_(?P<blk_id>\d+)/$',
        views.match, name='match'),
)