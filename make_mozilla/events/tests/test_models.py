from django.utils import unittest
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

class EventTest(unittest.TestCase):
    @patch.object(models.Event.objects, 'filter')
    def test_upcoming_events_can_be_retrieved(self, mock_query_set):
        mock_item = Mock()
        mock_query_set.return_value = [mock_item]
        mock_now = Mock()
        with patch('make_mozilla.events.models.datetime') as mock_datetime:
            mock_datetime.now.return_value = mock_now

            eq_(models.Event.upcoming(), [mock_item])

            mock_query_set.assert_called_with(start__gte = mock_now)

    # TO DO - do this with real DB objects...
    # @patch.object(models, 'Point')
    # @patch.object(models.Event.objects, 'filter')
    # def test_upcoming_events_can_be_retrieved(self, mock_query_set):
    #     pass
