# coding: utf-8

from django import http
from django_countries import countries
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.contrib.syndication.views import Feed
from django.contrib.gis.feeds import GeoRSSFeed
from django.utils.http import urlquote_plus, urlencode
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

import urllib2
import json
import bleach
import commonware
import jingo
from datetime import datetime
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

    try:
        current_campaign = models.Campaign.objects.get(pk=1)
    except ObjectDoesNotExist:
        current_campaign = None

    now = datetime.utcnow()

    featured = list(models.Event.objects.filter(official=True, end__gte=datetime.now(), pending_deletion=False).order_by('?')[:3])
    featured.sort(key=lambda event: event.start)

    return jingo.render(request, 'events/index.html', {
        'event_kinds': event_kinds,
        'current_campaign': current_campaign,
        'featured': featured,
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
        return http.HttpResponseRedirect(reverse('event', kwargs={'event_hash': event.hash}))

    return _render_event_creation_form(request, ef, vf, lf)


def verified_ownership(f):
    def wrapped(request, event_hash):
        event = get_object_or_404(models.Event, url_hash=event_hash)
        if not event.verify_ownership(request.user):
            return http.HttpResponseForbidden(u'sorry, you’re not allowed in')
        return f(request, event)
    return wrapped


@login_required
@verified_ownership
def edit_or_update(request, event):
    if request.method == "POST":
        ef, vf, lf = _process_create_post_data(request.POST)
        if ef.is_valid() and vf.is_valid():
            new_event = ef.instance
            new_event.organiser_email = event.organiser_email
            new_event.verified = event.verified
            new_event.official = event.official
            new_event.campaign = event.campaign
            new_event.source = event.source
            new_event.source_id = event.source_id
            new_venue = vf.instance
            vf.add_geo_data_to(new_venue)
            models.EventAndVenueUpdater.update(event, new_event, event.venue, new_venue)
            return http.HttpResponseRedirect(reverse('event', kwargs={'event_hash': event.hash}))
    else:
        ef = forms.EventForm(instance = event)
        vf = forms.VenueForm(instance = event.venue)
        lf = forms.PrivacyAndLegalForm()
    return _render_event_creation_form(request, ef, vf, lf, template = 'events/edit.html', event = event)

@login_required
@verified_ownership
def delete(request, event):
    if request.method == "POST":
        if event.bsd_hosted():
            event.pending_deletion = True
            event.save()
            return http.HttpResponseRedirect()
        else:
            event.delete()
            return http.HttpResponseRedirect(reverse('events.mine'))
    return jingo.render(request, 'events/delete.html', {'event': event})


def _render_event_creation_form(request, event_form, venue_form, privacy_and_legal_form, template = 'events/new.html', event = None):
    fieldsets = [
        forms.Fieldset(event_form, ('kind',)),
        forms.Fieldset(event_form, ('name', 'event_url', 'description', 'public')),
        forms.Fieldset(event_form, ('start', 'end',)),
        forms.Fieldset(venue_form, venue_form.fields),
    ]

    if event is None:
        fieldsets.append(privacy_and_legal_form)

    return jingo.render(request, template, {
        'fieldsets': tuple(fieldsets),
        'event': event
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


def from_id(request, event_id):
    event = get_object_or_404(models.Event, pk=event_id)
    return http.HttpResponseRedirect(reverse('event', kwargs={'event_hash': event.hash}))


def details(request, event_hash):
    event = get_object_or_404(models.Event, url_hash=event_hash)
    return jingo.render(request, 'events/detail.html', {'event': event})

@login_required
def mine(request):
    return jingo.render(request, 'events/mine.html', {
        'events': models.Event.all_user_non_bsd(request.user),
        'bsd_events': models.Event.all_user_bsd(request.user),
        'editable': True
    })


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


def all(request):
    today = datetime.today()
    page = request.GET.get('page', 1)

    if request.GET.get('sort') == 'name':
        sort, order = ('name', 'name')
    else:
        sort, order = ('date', 'start')

    results = models.Event.objects.filter(start__gte=today).order_by(order)
    results_per_page = 10

    return jingo.render(request, 'events/all.html', {
        'sort': sort,
        'results': paginators.results_page(results, results_per_page, page=page),
    })


class Country(object):
    def extract_page(self, request):
        return request.GET.get('page', 1)

    def extract_sort(self, request):
        sort = request.GET.get('sort')
        if sort == 'name':
            return ('name', 'name')
        else:
            return ('date', 'start')

    def paginated_results(self, latitude, longitude, order, results_per_page, page):
        results = models.Event.near(latitude, longitude, sort=order)
        return paginators.results_page(results, results_per_page, page=page)

    def render(self, request, country_code, template, results_per_page):
        try:
            country_list = dict(countries.COUNTRIES)
            country_name = country_list[country_code].__unicode__()
        except KeyError:
            raise http.Http404

        (sort, order) = self.extract_sort(request)
        page = self.extract_page(request)
        today = datetime.today()

        results = models.Event.objects.filter(start__gte=today, venue__country=country_code).order_by(order)

        return jingo.render(request, template, {
            'sort': sort,
            'country': {
                'code': country_code,
                'name': country_name,
            },
            'results': paginators.results_page(results, results_per_page, page=page),
        })

country_view = Country()


def country(request, code):
    return country_view.render(request, code.upper(), 'events/country-list.html', 4)


def country_map(request, code):
    return country_view.render(request, code.upper(), 'events/country-map.html', 999)


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
        results = models.Event.near(latitude, longitude, sort=order)
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
    return near_view.render(request, 'events/near-map.html', 999)


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
            {
                'campaign': campaign,
                'partners': campaign.partner_set.all()
            })


def guides_all(request):
    event_kinds = models.EventKind.objects.all()
    events_dict = dict([(o.slug, o) for o in event_kinds])
    return jingo.render(request, 'events/guides/index.html', {
        'event_kinds': events_dict,
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


def scribble_live(request):
    return jingo.render(request, 'events/live-updates.html', {})
