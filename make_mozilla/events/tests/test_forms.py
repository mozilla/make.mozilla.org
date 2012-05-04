from django.utils import unittest
from nose.tools import eq_, ok_

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

    def test_does_not_expose_organiser_email(self):
        self.assertNotIn('organiser_email', self.f.fields)

    def test_does_not_expose_verified(self):
        self.assertNotIn('verified', self.f.fields)

    def test_does_not_expose_official(self):
        self.assertNotIn('official', self.f.fields)

    def test_does_not_expose_source_id(self):
        self.assertNotIn('source_id', self.f.fields)

    def test_does_not_expose_campaign(self):
        self.assertNotIn('campaign', self.f.fields)

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

    def test_that_an_instance_with_the_good_data_is_valid(self):
        good_data = {
            'venue-name': 'Test Venue',
            'venue-street_address': '100 Test Street',
            'venue-country': 'GB',
            'venue-latitude': '51.0',
            'venue-longitude': '0.5'
        }
        ok_(forms.VenueForm(good_data).is_valid())

    def test_that_an_instance_without_lat_lon_is_invalid(self):
        data = {
            'venue-name': 'Test Venue',
            'venue-street_address': '100 Test Street',
            'venue-country': 'GB',
        }
        ok_(not forms.VenueForm(data).is_valid())

