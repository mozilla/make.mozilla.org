from django import forms
from make_mozilla.events import models, widgets

class Fieldset(object):
    def __init__(self, form, fields, legend=None, className=None):
        self.form = form
        self.fields = fields
        self.legend = legend
        self.className = className

    def __iter__(self):
        for name in self.fields:
            field = self.form.fields[name]
            yield forms.forms.BoundField(self.form, field, name)

class PrefixedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrefixedModelForm, self).__init__(*args, **kwargs)
        self.prefix = self.field_prefix

class EventForm(PrefixedModelForm):
    field_prefix = 'event'
    kind = forms.ModelChoiceField(queryset=models.EventKind.objects.all(),
                empty_label=None,
                label='Choose event type',
                widget=forms.RadioSelect,
                error_messages={'required': 'Please select an event type'})
    name = forms.CharField(label='Name your event')
    event_url = forms.URLField(label='Event URL', widget=widgets.UrlInput(attrs={'placeholder': 'http://'}), required=False)
    public = forms.BooleanField(help_text='This event should be made available in search results.', required=False)

    class Meta:
        model = models.Event
        fields = ('name', 'description', 'event_url', 'start', 'end', 'kind', 'public')
        widgets = {
            'start': widgets.SplitDateTimeWidget(attrs={'date_placeholder': 'Date', 'time_placeholder': 'Time'}),
            'end': widgets.SplitDateTimeWidget(attrs={'date_placeholder': 'Date', 'time_placeholder': 'Time'}),
        }

class VenueForm(PrefixedModelForm):
    field_prefix = 'venue'
    name = forms.CharField(label='Venue Name')
    latitude = forms.FloatField(widget=forms.HiddenInput)
    longitude = forms.FloatField(widget=forms.HiddenInput)

    class Meta:
        model = models.Venue
        exclude = ('location',)
