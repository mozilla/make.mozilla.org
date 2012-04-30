from django import forms
from make_mozilla.events import models

class PrefixedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrefixedModelForm, self).__init__(*args, **kwargs)
        self.prefix = self.field_prefix

class EventForm(PrefixedModelForm):
    field_prefix = 'event'

    class Meta:
        model = models.Event
        fields = ('name', 'event_url', 'start', 'end', 'kind')

class VenueForm(PrefixedModelForm):
    field_prefix = 'venue'
    latitude = forms.FloatField()
    longitude = forms.FloatField()

    class Meta:
        model = models.Venue
        exclude = ('location',)
