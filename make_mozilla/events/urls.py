from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^events/new$',              'make_mozilla.events.views.event.new'),
    url(r'^events/create$',           'make_mozilla.events.views.event.create', name = 'create-event'),
    url(r'^events/(?P<event_id>.+)$', 'make_mozilla.events.views.event.detail'),
)
