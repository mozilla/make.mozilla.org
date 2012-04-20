from django.conf.urls.defaults import patterns, url
from make_mozilla.events.views import events

urlpatterns = patterns('',
    url(r'^$',                 events.index,   name = 'events'),
    url(r'^new/$',              events.new,    name = 'event.new'),
    url(r'^create/$',           events.create, name = 'event.create'),
    url(r'^(?P<event_id>.+)/$', events.details, name = 'event'),
)
