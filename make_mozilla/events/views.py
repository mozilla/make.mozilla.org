from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.http import urlquote_plus, urlencode
from django.views.decorators.csrf import csrf_protect

import urllib2
import json
import bleach
import commonware
import jingo
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf

from django.conf import settings
from make_mozilla.events import forms
from make_mozilla.events import models
from make_mozilla.events import tasks
from make_mozilla.events import paginators

log = commonware.log.getLogger('playdoh')


# Workaround from http://gis.stackexchange.com/questions/7553/is-there-a-geodjango-tutorial-for-georssfeeds
class IndexGeoRSSFeed(Feed):
    title = "Make Mozilla!"
    link = '/events/'
    description = "Updates on upcoming events"
    feed_type = GeoRSSFeed

    def items(self):
        return models.Event.upcoming()

    def item_extra_kwargs(self, item):
        return {'geometry': self.item_geometry(item)}

    def item_geometry(self, item):
        return item.location


def index(request):
    event_kinds = models.EventKind.objects.all()
    return jingo.render(request, 'events/index.html', {'event_kinds': event_kinds})


@login_required
def new(request):
    return render_event_creation_form(request, forms.EventForm(), forms.VenueForm())


def search(request):
    location = request.GET.get('location')

    if location:
        url="http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % urlquote_plus(location)
        response = urllib2.urlopen(url)
        results = json.loads(response.read()).get('results', ())
    else:
        results = ()

    if len(results) == 1:
        return http.HttpResponseRedirect("%s?%s" % (reverse('events.near'), urlencode({
            'lat': results[0].get('geometry',{}).get('location',{}).get('lat',''),
            'lng': results[0].get('geometry',{}).get('location',{}).get('lng',''),
        })))

    return jingo.render(request, 'events/search.html', {'results': results, 'location': location})


def details(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    return jingo.render(request, 'events/detail.html', {'event': event})


@require_POST
@login_required
def create(request):
    ef, vf = process_create_post_data(request.POST)
    if ef.is_valid() and vf.is_valid():
        event, venue = create_event_and_venue(request.user, ef, vf)
        return http.HttpResponseRedirect(reverse('event', kwargs={'event_id': event.id}))

    return render_event_creation_form(request, ef, vf)


def render_event_creation_form(request, event_form, venue_form):
    fieldsets = (
        forms.Fieldset(event_form, ('kind',)),
        forms.Fieldset(event_form, ('name', 'event_url', 'description', 'public')),
        forms.Fieldset(event_form, ('start', 'end',)),
        forms.Fieldset(venue_form, venue_form.fields),
    )

    return jingo.render(request, 'events/new.html', {
        # 'event_form': event_form,
        # 'venue_form': venue_form,
        'fieldsets': fieldsets
    })


def process_create_post_data(data):
    event_form = forms.EventForm(data)
    venue_form = forms.VenueForm(data)
    return (event_form, venue_form)


def create_event_and_venue(user, event_form, venue_form):
    venue = venue_form.save()
    event = event_form.instance
    event.venue = venue
    organiser_email = user.email
    event.organiser_email = organiser_email
    tasks.register_email_address_as_constituent.delay(organiser_email, '111')
    event.save()
    return (event, venue)


class Near(object):
    def extract_latlon(self, request):
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        return (latitude, longitude)

    def extract_page(self, request):
        return request.GET.get('page', 1)

    def paginated_results(self, latitude, longitude, results_per_page, page):
        results = models.Event.near(latitude, longitude)
        return paginators.results_page(results, results_per_page, page=page)

    def render(self, request, template, results_per_page):
        (lat, lon) = self.extract_latlon(request)
        page = self.extract_page(request)

        return jingo.render(request, template, {
            'latitude': lat,
            'longitude': lon,
            'results': self.paginated_results(lat, lon, results_per_page, page)
        })

near_view = Near()


@require_GET
def near(request):
    return near_view.render(request, 'events/near-list.html', 4)


@require_GET
def near_map(request):
    return near_view.render(request, 'events/near-map.html', 24)


def guides_all(request):
    event_kinds = models.EventKind.objects.all()
    return jingo.render(request, 'events/guides/index.html', {
        'event_kinds': event_kinds,
    })


def guides_template(request): 
    return jingo.render(request, 'events/guides/template.html', {})
