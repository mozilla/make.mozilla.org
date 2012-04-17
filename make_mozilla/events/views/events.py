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

log = commonware.log.getLogger('playdoh')

def new(request):
    new_event_form = forms.EventForm()
    new_venue_form = forms.VenueForm()
    return jingo.render(request, 'events/new.html', {
        'event_form': new_event_form,
        'venue_form': new_venue_form
    })

@require_POST
def create(request):
    pass
