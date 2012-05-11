from django.conf.urls.defaults import patterns, url
from make_mozilla.events import views

urlpatterns = patterns('',
    url(r'^$',                      views.index,                name='events'),
    url(r'^feed.rss$',              views.IndexGeoRSSFeed(),    name='events-feed'),
    url(r'^new/$',                  views.new,                  name='event.new'),
    url(r'^create/$',               views.create,               name='event.create'),
    url(r'^near/$',                 views.near,                 name='events.near'),
    url(r'^near/map/$',             views.near_map,             name='events.near.map'),
    url(r'^search/$',               views.search,               name='events.search'),
    url(r'^about/$',                views.about,                name='about'),
    url(r'^about/partners/$',       views.partners,             name='partners', kwargs={'slug': 'summer_campaign'}),
    url(r'^guides/$',               views.guides_all,           name='guides_all'),
    url(r'^guides/kitchen-table/$', views.guides_kitchen_table, name='guides_kitchen_table'),
    url(r'^guides/hack-jam/$',      views.guides_hack_jam,      name='guides_hack_jam'),
    url(r'^guides/pop-up/$',        views.guides_pop_up,        name='guides_pop_up'),
    url(r'^(?P<event_id>\d+)/$',    views.details,              name='event'),
)
