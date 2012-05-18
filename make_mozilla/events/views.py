from django import http
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.http import urlquote_plus, urlencode
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, get_object_or_404

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
    current_campaign = models.Campaign.current()

    return jingo.render(request, 'events/code-party_splash.html', {
        'event_kinds': event_kinds,
        'current_campaign': current_campaign,
    })


@login_required
def new(request):
    return _render_event_creation_form(request, forms.EventForm(), forms.VenueForm(), forms.PrivacyAndLegalForm())


@require_POST
@login_required
def create(request):
    ef, vf, lf = _process_create_post_data(request.POST)
    if lf.is_valid() and ef.is_valid() and vf.is_valid():
        event, venue = _create_event_and_venue(request.user, ef, vf)
        _add_email_to_bsd(request.user, lf)
        return http.HttpResponseRedirect(reverse('event', kwargs={'event_id': event.id}))

    return _render_event_creation_form(request, ef, vf, lf)


def _render_event_creation_form(request, event_form, venue_form, privacy_and_legal_form):
    fieldsets = (
        forms.Fieldset(event_form, ('kind',)),
        forms.Fieldset(event_form, ('name', 'event_url', 'description', 'public')),
        forms.Fieldset(event_form, ('start', 'end',)),
        forms.Fieldset(venue_form, venue_form.fields),
        privacy_and_legal_form,
    )

    return jingo.render(request, 'events/new.html', {
        'fieldsets': fieldsets
    })


def _process_create_post_data(data):
    event_form = forms.EventForm(data)
    venue_form = forms.VenueForm(data)
    privacy_and_legal_form = forms.PrivacyAndLegalForm(data)
    return (event_form, venue_form, privacy_and_legal_form)


def _create_event_and_venue(user, event_form, venue_form):
    venue = venue_form.save()
    event = event_form.instance
    event.venue = venue
    organiser_email = user.email
    event.organiser_email = organiser_email
    event.save()
    return (event, venue)


def _add_email_to_bsd(user, privacy_form):
    if privacy_form.cleaned_data['add_me_to_email_list']:
        tasks.register_email_address_as_constituent.delay(user.email, '111')


def details(request, event_id):
    event = get_object_or_404(models.Event, pk=event_id)
    return jingo.render(request, 'events/detail.html', {'event': event})


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


class Near(object):
    def extract_latlon(self, request):
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lng')
        return (latitude, longitude)

    def extract_page(self, request):
        return request.GET.get('page', 1)

    def extract_sort(self, request):
        sort = request.GET.get('sort')
        if sort == 'name':
            return ('name', 'name')
        else:
            return ('date', 'start')

    def paginated_results(self, latitude, longitude, order, results_per_page, page):
        results = models.Event.near(latitude, longitude, sort = order)
        return paginators.results_page(results, results_per_page, page=page)

    def render(self, request, template, results_per_page):
        (lat, lon) = self.extract_latlon(request)
        (sort, order) = self.extract_sort(request)
        page = self.extract_page(request)

        try:
            results = self.paginated_results(lat, lon, order, results_per_page, page)
        except TypeError, ValueError:
            return redirect('events.search')

        return jingo.render(request, template, {
            'latitude': lat,
            'longitude': lon,
            'sort': sort,
            'results': results
        })

near_view = Near()


@require_GET
def near(request):
    return near_view.render(request, 'events/near-list.html', 4)


@require_GET
def near_map(request):
    return near_view.render(request, 'events/near-map.html', 24)


@require_GET
def campaign(request, slug):
    campaign = get_object_or_404(models.Campaign, slug=slug)
    return jingo.render(request, 'events/campaign.html',
        {'campaign': campaign, 'partners': campaign.partner_set.filter(featured=True)}
    )


@require_GET
def partners(request, slug):
    campaign = get_object_or_404(models.Campaign, slug=slug)
    return jingo.render(request, 'events/partners.html', 
            {'campaign': campaign, 'partners': campaign.partner_set.all()})


def guides_all(request):
    event_kinds = models.EventKind.objects.all()
    return jingo.render(request, 'events/guides/index.html', {
        'event_kinds': event_kinds,
    })


def guides_kitchen_table(request):
    page_data = models.EventKind.objects.get(slug='kitchen_table')
    return jingo.render(request, 'events/guides/kitchen-table.html', {
        'page_data': page_data,
    })


def guides_hack_jam(request):
    page_data = models.EventKind.objects.get(slug='hack_jam')
    return jingo.render(request, 'events/guides/hack-jam.html', {
        'page_data': page_data,
    })


def guides_pop_up(request):
    page_data = models.EventKind.objects.get(slug='pop_up')
    return jingo.render(request, 'events/guides/pop-up.html', {
        'page_data': page_data,
    })


def privacy_policy(request):
    return jingo.render(request, 'events/legal/privacy.html', {})


def terms(request):
    return jingo.render(request, 'events/legal/terms.html', {})


def content_guidelines(request):
    return jingo.render(request, 'events/legal/content.html', {})


def event_guidelines(request):
    return jingo.render(request, 'events/legal/guidelines.html', {})
