import logging

from django import http
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.forms import ModelForm
from make_mozilla.base import models


import bleach
import commonware
from funfactory.log import log_cef
from mobility.decorators import mobile_template
from session_csrf import anonymous_csrf

log = commonware.log.getLogger('playdoh')

class EventForm(ModelForm):
    class Meta:
        model = models.Event

@anonymous_csrf
def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = EventForm(request.POST) # A form bound to the POST data
        print form
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            pass
        return HttpResponseRedirect(url('event', {'event_id': 'x'})) # Redirect after POST
    return render(request, 'root/index.html', data)

def detail(request, event_id):
    return render_to_response('event/detail.html', {})

def new(request):
    new_event_form = EventForm()
    return render(request, 'event/new.html', {'form': new_event_form})

