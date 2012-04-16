from django import forms
from make_mozilla.events import models

class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event

class VenueForm(forms.ModelForm):
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = models.Venue
        exclude = ('location',)
