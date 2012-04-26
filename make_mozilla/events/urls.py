from django.conf.urls.defaults import patterns, url
from make_mozilla.events import views

urlpatterns = patterns('',
    url(r'^$',                  views.index,             name = 'events'),
    url(r'^feed.rss$',          views.IndexGeoRSSFeed(), name = 'events-feed'),
    url(r'^new/$',              views.new,               name = 'event.new'),
    url(r'^create/$',           views.create,            name = 'event.create'),
    url(r'^near/$',             views.near,              name = 'events.near'),
    url(r'^near/list/$',        views.near_list,         name = 'events.near.list'),
    url(r'^(?P<event_id>.+)/$', views.details,           name = 'event'),
)
