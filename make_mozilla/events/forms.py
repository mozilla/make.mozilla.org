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

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)

        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['latitude'] = instance.latitude
            self.initial['longitude'] = instance.longitude 

    def save(self, commit=True):
        model = super(VenueForm, self).save(commit=False)

        model.latitude = self.cleaned_data['latitude']
        model.longitude = self.cleaned_data['longitude']

        if commit:
            model.save()

        return model

    def clean(self):
        cleaned_data = self.cleaned_data
        if not cleaned_data.has_key('latitude') or not cleaned_data.has_key('longitude'):
            self._errors['street_address'] = self.error_class(["We can't find your address"])
            del cleaned_data['street_address']
        return cleaned_data

    class Meta:
        model = models.Venue
        exclude = ('location',)
