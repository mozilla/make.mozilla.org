from django.forms import ModelForm

from make_mozilla.events import models

class VenueForm(ModelForm):
    class Meta:
        model = models.Venue
