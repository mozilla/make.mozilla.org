from django.utils import unittest

from make_mozilla.events import models, forms

class VenueFormTest(unittest.TestCase):
    def test_exposes_latitude(self):
        f = forms.VenueForm()
        self.assertTrue(f.fields.has_key('latitude'))

    def test_exposes_longitude(self):
        f = forms.VenueForm()
        self.assertTrue(f.fields.has_key('longitude'))

    def test_does_not_expose_location(self):
        f = forms.VenueForm()
        self.assertNotIn('location', f.fields)
