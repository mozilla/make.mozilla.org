from django.utils import unittest

from make_mozilla.events import models, forms

class EgPrefixedModelForm(forms.PrefixedModelForm):
    field_prefix = 'prefix'
    class Meta:
        model = models.Event

class PrefixedModelFormTest(unittest.TestCase):
    def test_sets_prefix_correctly(self):
        self.assertEqual('prefix', EgPrefixedModelForm().prefix)

class EventFormTest(unittest.TestCase):
    def setUp(self):
        self.f = forms.EventForm()

    def test_has_correct_prefix(self):
        self.assertEqual('event', self.f.prefix)

    def test_does_not_expose_venue(self):
        self.assertNotIn('venue', self.f.fields)

class VenueFormTest(unittest.TestCase):
    def setUp(self):
        self.f = forms.VenueForm()

    def test_has_correct_prefix(self):
        self.assertEqual('venue', self.f.prefix)

    def test_exposes_latitude(self):
        self.assertTrue(self.f.fields.has_key('latitude'))

    def test_exposes_longitude(self):
        self.assertTrue(self.f.fields.has_key('longitude'))

    def test_does_not_expose_location(self):
        self.assertNotIn('location', self.f.fields)
