from django.utils import unittest
import django.test
from nose.tools import eq_, ok_
from mock import patch, Mock
from django.contrib.gis import geos
import datetime

from make_mozilla.events import models
from django.contrib.auth import models as auth_models

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

    def test_lat_lng_can_be_set_on_instantiation(self):
        venue = models.Venue(latitude = "51.0", longitude = "4")

        eq_(venue.location, geos.Point(4.0, 51.0))

class EventTestHelperMixin(object):
    def add_event(self, name, venue, offset, public = True, verified = True, pending_deletion = False):
        start = datetime.datetime.now() + datetime.timedelta(days = offset)
        end = start + datetime.timedelta(hours = 3)
        e = models.Event(name = name, venue = venue, organiser_email = 'moz@example.com',
                start = start, end = end, public = public, verified = verified, pending_deletion = pending_deletion)
        e.save()
        return e

    def add_bsd_event(self, name, venue, offset, bsd_id):
        e = self.add_event(name, venue, offset)
        e.source = 'bsd'
        e.source_id = bsd_id
        e.save()
        return e

    def setup_events(self):
        london = models.Venue(name = "Test Venue", street_address = "0 Somewhere St", 
                country = "GB")
        london.latitude = 51.510345
        london.longitude = -0.127072
        london.save()
        berlin = models.Venue(name = "Berlin test Venue", street_address = "Somewhere Str. 0", 
                country = "DE")
        berlin.latitude = 52.50693980
        berlin.longitude = 13.42415920
        berlin.save()

        e1 = self.add_event("E1", london, 3)
        e2 = self.add_event("E2", berlin, 2)
        e3 = self.add_event("E3", london, 1)

        eu = self.add_event("EU", berlin, 9, verified = False)
        ep = self.add_event("EP", berlin, 10, public = False)
        ed = self.add_event("ED", london, 8, pending_deletion = True)

        return (e1, e2, e3, ep)



class EventTest(django.test.TestCase, EventTestHelperMixin):
    def test_upcoming_public_events_can_be_retrieved(self):
        (e1, e2, e3, ep) = self.setup_events()
        actual = models.Event.upcoming()
        eq_(len(actual), 3)
        ok_(e1.id in [x.id for x in actual])
        ok_(e2.id in [x.id for x in actual])

    def test_upcoming_events_near_london_can_be_retrieved(self):
        (e1, e2, e3, ep) = self.setup_events()
        actual = models.Event.near(51.5154460, -0.13165810, sort = 'start')
        eq_([x.name for x in actual], ["E3", "E1"])

    def test_upcoming_events_can_be_ordered_by_name(self):
        self.setup_events()
        actual = models.Event.upcoming(sort = 'name')
        eq_([x.name for x in actual], ["E1", "E2", "E3"])

    def test_all_upcoming_events_near_berlin_can_be_retrieved(self):
        self.setup_events()
        actual = models.Event.near(52.50693980, 13.42415920, sort = 'start', include_private = True)
        eq_([x.name for x in actual], ["E2", "EP"])

    def test_that_an_event_can_verify_its_creator(self):
        e = models.Event(name = 'An Event', organiser_email = 'moz@example.com')
        user = auth_models.User(email = 'moz@example.com')
        assert e.verify_ownership(user)

    def test_that_an_event_can_verify_a_user_is_not_its_creator(self):
        e = models.Event(name = 'An Event', organiser_email = 'moz@example.com')
        user = auth_models.User(email = 'boz@example.com')
        assert not e.verify_ownership(user)

class UserEventListTest(django.test.TestCase, EventTestHelperMixin):
    def setUp(self):
        berlin = models.Venue(name = "Berlin test Venue", street_address = "Somewhere Str. 0", 
                country = "DE")
        berlin.latitude = 52.50693980
        berlin.longitude = 13.42415920
        berlin.save()
        self.user = Mock()
        self.user.email = 'moz@example.com'
        self.e1 = self.add_event("E1", berlin, 3)
        self.e2 = self.add_event("E2", berlin, 2)
        self.e3 = self.add_bsd_event("E3", berlin, 1, 'jjj')

    def test_that_all_a_users_non_bsd_events_can_be_fetched(self):
        actual = models.Event.all_user_non_bsd(self.user)
        eq_([x.name for x in actual], ["E2", "E1"])

    def test_that_all_a_users_bsd_events_can_be_fetched(self):
        actual = models.Event.all_user_bsd(self.user)
        eq_([x.name for x in actual], ["E3"])

class TestEventAndVenueUpdater(unittest.TestCase):
    def test_that_identical_model_instances_can_be_compared_properly(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = 1, name = "Hallo")

        ok_(models.EventAndVenueUpdater.are_model_instances_identical(e1, e2))

    def test_that_non_identical_model_instances_compare_false(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = 1, name = "Boo hoo")

        ok_(not models.EventAndVenueUpdater.are_model_instances_identical(e1, e2))

    def test_that_model_instances_of_different_classes_compare_false(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Venue(id = 1, name = "Hallo")

        ok_(not models.EventAndVenueUpdater.are_model_instances_identical(e1, e2))

    def test_that_unset_ids_are_ignored_when_comparing_instances(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = None, name = "Hallo")

        ok_(models.EventAndVenueUpdater.are_model_instances_identical(e1, e2))
