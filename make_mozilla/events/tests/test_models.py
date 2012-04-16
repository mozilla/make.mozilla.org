from django.utils import unittest
from django.contrib.gis import geos

from make_mozilla.events import models

class VenueTest(unittest.TestCase):
    def test_location_is_always_initialized_as_a_point_object(self):
        venue = models.Venue()
        self.assertIsNotNone(venue.location.wkt)

    def test_latitude_can_be_set(self):
        venue = models.Venue()
        venue.latitude = 51.456

        self.assertEqual(venue.location, geos.Point(51.456, 0))
    
    def test_latitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        self.assertEqual(venue.latitude, 42.0)

    def test_longitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        self.assertEqual(venue.longitude, 24.0)

    def test_longitude_can_be_set(self):
        venue = models.Venue()
        venue.longitude = 51.456

        self.assertEqual(venue.location, geos.Point(0, 51.456))
