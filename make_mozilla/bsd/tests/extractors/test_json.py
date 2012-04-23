from django.utils import unittest
from mock import patch, Mock
from nose.tools import eq_, ok_
import pytz
from datetime import datetime
from make_mozilla.base.tests.decorators import wip
from make_mozilla.bsd.tests.utils import json_fixture

from make_mozilla.bsd.extractors import json as extractors

def ef():
    return json_fixture('event.json')

class EventExtractorTest(unittest.TestCase):
    def test_name_is_extracted_correctly(self):
        eq_(extractors.event_name(ef()),
            {'name': 'Test kitchen table event'})

    def test_time_is_extracted_correctly(self):
        pst = pytz.timezone('America/Vancouver')
        expected_start = pst.localize(datetime(2012, 04, 17, 18, 0, 0))
        expected_end   = pst.localize(datetime(2012, 04, 17, 21, 0, 0))
        eq_(extractors.event_times(ef()),
            {'start': expected_start, 'end': expected_end})

class VenueExtractorTest(unittest.TestCase):
    def test_name_is_extracted_correctly(self):
        eq_(extractors.venue_name(ef()),
            {'name': 'Mozilla Mountain View'})

    def test_country_is_extracted_correctly(self):
        eq_(extractors.venue_country(ef()), {'country': 'US'})

    def test_street_address_is_extracted_correctly(self):
        eq_(extractors.venue_street_address(ef()), 
            {'street_address': '650 Castro Street\n3rd Floor: 10 Fwd\nMountain View\nCA\n94041'})

    def test_location_is_extracted_correctly(self):
        eq_(extractors.venue_location(ef()),
            {'latitude': 37.388096, 'longitude': -122.082764})

# class ExtractTest(unittest.TestCase):
