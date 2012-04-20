import os.path
from django.utils import unittest
from mock import patch, Mock
from nose.tools import eq_, ok_

from make_mozilla import bsd
import urllib2
import json

def fixture_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def json_fixture(fixture_name):
    return json.load(open(fixture_path('fixtures/%s' % fixture_name)))

class BSDEventFeedParserTest(unittest.TestCase):
    @patch.object(bsd, 'process_events_json')
    @patch.object(json, 'load')
    @patch.object(urllib2, 'urlopen')
    def test_event_feed_parser_invokes_the_url_fetcher_correctly(self, 
            mock_urlopen, mock_json_loader, mock_process_events_func):
        mock_urlopen_io = Mock()
        mock_urlopen.return_value = mock_urlopen_io
        mock_json_loader.return_value = {'mock_json_feed': True}
        mock_process_events_func.return_value = ['bsd_api_id']

        actual = bsd.parse_event_feed('http://example.com/feed.json')

        mock_urlopen.assert_called_with('http://example.com/feed.json')
        mock_json_loader.assert_called_with(mock_urlopen_io)
        mock_process_events_func.assert_called_with({'mock_json_feed': True})
        eq_(['bsd_api_id'], actual)

    def test_event_feed_parser_returns_6_events(self):
        actual = bsd.process_events_json(json_fixture('event_feed.json'))

        eq_(6, len(actual))

    def test_event_feed_parser_returns_the_right_ids(self):
        actual = bsd.process_events_json(json_fixture('event_feed.json'))

        eq_(['981', '983', '974', '971', '975', '936'], actual)

class BSDEventImporterTest(unittest.TestCase):
    @patch.object(bsd.BSDEventImporter, 'venue_extractors')
    @patch.object(bsd.BSDEventImporter, 'event_extractors')
    def test_relevant_information_is_extracted_from_event_json(self, mock_event_extractors, mock_venue_extractors):
        event_json = json_fixture('event.json')
        actual = bsd.BSDEventImporter.extract_from_event_json(event_json )
        mock_event_extractor = Mock()
        mock_venue_extractor = Mock()
        mock_event_extractors.return_value = [mock_event_extractor]
        mock_venue_extractors.return_value = [mock_venue_extractor]
        mock_event_extractor.return_value = {1: 1}
        mock_venue_extractor.return_value = {2: 2}

        expected = {'event': {1: 1}, 'venue': {2: 2}}

        mock_event_extractor.assert_called_with(event_json)
        eq_(expected, actual)

