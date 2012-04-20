import os.path
from django.utils import unittest
from mock import patch, Mock
from nose.tools import eq_, ok_

from make_mozilla import bsd
import urllib2
import json

def fixture_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def json_fixture():
    return json.load(open(fixture_path('fixtures/event_feed.json')))

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
        actual = bsd.process_events_json(json_fixture())

        eq_(6, len(actual))

    def test_event_feed_parser_returns_the_right_ids(self):
        actual = bsd.process_events_json(json_fixture())

        eq_(['981', '983', '974', '971', '975', '936'], actual)
