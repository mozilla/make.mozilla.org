from django.conf.urls.defaults import patterns, url
from make_mozilla.events import views

urlpatterns = patterns('',
    url(r'^$',                     views.index,             name='events'),
    url(r'^feed.rss$',             views.IndexGeoRSSFeed(), name='events-feed'),
    url(r'^new/$',                 views.new,               name='event.new'),
    # url(r'^create/$',              views.create,            name='event.create'),
    url(r'^near/$',                views.near,              name='events.near'),
    url(r'^near/map/$',            views.near_map,          name='events.near.map'),
    url(r'^search/$',              views.search,            name='events.search'),
    url(r'^guides/$',              views.guides_all,        name='guides_all'),
    url(r'^guides/inner/$',        views.guides_template,   name='guides_template'),
    url(r'^(?P<event_id>[^/]+)/$', views.details,           name='event'),
)
