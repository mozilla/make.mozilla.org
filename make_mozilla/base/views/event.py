from django import http
from django.forms import ModelForm
from django.core.urlresolvers import reverse

import bleach
import commonware
import jingo
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf

from make_mozilla.base import models


from django.conf import settings

log = commonware.log.getLogger('playdoh')

class EventForm(ModelForm):
    class Meta:
        model = models.Event

@anonymous_csrf
def create(request):
    print settings.DEFAULT_CHARSET
    if request.method == 'POST': # If the form has been submitted...
        form = EventForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            return http.HttpResponseRedirect(
                reverse('make_mozilla.base.views.event.detail', kwargs={'event_id': event.pk})
            ) # Redirect after POST
    return jingo.render(request, 'event/new.html', {'form': form})

def detail(request, event_id):
    event = models.Event.objects.get(pk=event_id)
    return jingo.render(request, 'event/detail.html', {'event': event})

def new(request):
    new_event_form = EventForm()
    return jingo.render(request, 'event/new.html', {'form': new_event_form})

