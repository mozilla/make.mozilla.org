from django.conf.urls.defaults import patterns, url
from django.views.generic import RedirectView
from make_mozilla.events import views
from make_mozilla.events import models

summer_campaign_slug = 'summer-code-party'
first_campaign_horrid_hack_list = list(models.Campaign.objects.all()[:1])
if len(first_campaign_horrid_hack_list) > 0:
    summer_campaign_slug = first_campaign_horrid_hack_list[0].slug

about_redirect = RedirectView.as_view(url='/events/about/%s/' % summer_campaign_slug)

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='events'),
    url(r'^feed.rss$',
        views.IndexGeoRSSFeed(),    name='events-feed'),
    url(r'^new/$',
        views.new,                  name='event.new'),
    url(r'^create/$',
        views.create,               name='event.create'),
    url(r'^near/$',
        views.near,                 name='events.near'),
    url(r'^near/map/$',
        views.near_map,             name='events.near.map'),
    url(r'^search/$',
        views.search,               name='events.search'),
    url(r'^about/$',
        about_redirect,             name='about'),
    url(r'^about/(?P<slug>[a-z0-9_-]+)/$',
        views.campaign,             name='campaign'),
    url(r'^about/(?P<slug>[a-z0-9_-]+)/partners/$',
        views.partners,             name='partners'),
    url(r'^legal/privacy-policy/$',
        views.privacy_policy,       name='events_privacy'),
    url(r'^legal/terms-of-use/$',
        views.terms,                name='events_terms'),
    url(r'^legal/content-guidelines/$',
        views.content_guidelines,   name='events_content'),
    url(r'^legal/event-guidelines/$',
        views.event_guidelines,   name='events_guidelines'),
    url(r'^guides/$',
        views.guides_all,           name='guides_all'),
    url(r'^guides/kitchen-table/$',
        views.guides_kitchen_table, name='guides_kitchen_table'),
    url(r'^guides/hack-jam/$',
        views.guides_hack_jam,      name='guides_hack_jam'),
    url(r'^guides/pop-up/$',
        views.guides_pop_up,        name='guides_pop_up'),
    url(r'^(?P<event_id>\d+)/$',
        views.from_id,              name='event.from_id'),
    url(r'^(?P<event_hash>[a-z0-9]{9,})/$',
        views.details,              name='event')
)
