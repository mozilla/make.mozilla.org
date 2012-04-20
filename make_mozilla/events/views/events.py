from django import http
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST

import bleach
import commonware
import jingo
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf

from django.conf import settings
from make_mozilla.events import forms
from make_mozilla.events import models

log = commonware.log.getLogger('playdoh')

def index(request):
    return jingo.render(request, 'events/splash.html', {})

def new(request):
    new_event_form = forms.EventForm()
    new_venue_form = forms.VenueForm()
    return jingo.render(request, 'events/new.html', {
        'event_form': new_event_form,
        'venue_form': new_venue_form
    })

def details(request, event_id):
    event = models.Event.objects.get(pk = event_id)
    return jingo.render(request, 'events/detail.html', {'event': event})

@require_POST
def create(request):
    ef, vf = process_create_post_data(request.POST)
    if ef.is_valid() and vf.is_valid():
        event, venue = create_event_and_venue(ef, vf)
        return http.HttpResponseRedirect(reverse('event', kwargs = {'event_id': event.id}))
    return jingo.render(request, 'events/new.html', {
        'event_form': ef,
        'venue_form': vf
    })

def process_create_post_data(data):
    event_form = forms.EventForm(data)
    venue_form = forms.VenueForm(data)
    return (event_form, venue_form)

def create_event_and_venue(event_form, venue_form):
    venue = venue_form.save()
    event = event_form.save(commit = False)
    event.venue = venue
    event.save()
    return (event, venue)
