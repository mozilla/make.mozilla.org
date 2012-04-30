from django.utils import unittest
import django.test
from nose.tools import eq_, ok_
from mock import patch, Mock
from django.contrib.gis import geos
import datetime

from make_mozilla.events import models

class VenueTest(unittest.TestCase):
    def test_location_is_always_initialized_as_a_point_object(self):
        venue = models.Venue()
        self.assertIsNotNone(venue.location.wkt)

    def test_latitude_can_be_set(self):
        venue = models.Venue()
        venue.latitude = 51.456

        eq_(venue.location, geos.Point(0, 51.456))
    
    def test_latitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        eq_(venue.latitude, 24.0)

    def test_longitude_can_be_gotten(self):
        venue = models.Venue(location = geos.Point(42, 24))

        eq_(venue.longitude, 42.0)

    def test_longitude_can_be_set(self):
        venue = models.Venue()
        venue.longitude = 51.456

        eq_(venue.location, geos.Point(51.456, 0))

class EventTest(django.test.TestCase):
    def setup_events(self):
        london = models.Venue(name = "Test Venue", street_address = "0 Somewhere St", 
                country = "UK")
        london.latitude = 51.510345
        london.longitude = -0.127072
        london.save()
        berlin = models.Venue(name = "Berlin test Venue", street_address = "Somewhere Str. 0", 
                country = "Germany")
        berlin.latitude = 52.50693980
        berlin.longitude = 13.42415920
        berlin.save()

        start = datetime.datetime.now() + datetime.timedelta(days = 1)
        end = start + datetime.timedelta(hours = 3)

        e1 = models.Event(name = "E1", venue = london, organiser_email = 'moz@example.com',
                start = start, end = end)
        e1.save()
        e2 = models.Event(name = "E2", venue = berlin, organiser_email = 'moz@example.com',
                start = start, end = end)
        e2.save()

        return (e1, e2)

    def test_upcoming_events_can_be_retrieved(self):
        (e1, e2) = self.setup_events()
        actual = models.Event.upcoming()
        eq_(len(actual), 2)
        ok_(e1.id in [x.id for x in actual])
        ok_(e2.id in [x.id for x in actual])

    def test_upcoming_events_near_london_can_be_retrieved(self):
        (e1, e2) = self.setup_events()
        actual = models.Event.near(51.5154460, -0.13165810)
        eq_(len(actual), 1)
        eq_(actual[0].id, e1.id)
