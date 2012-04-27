import os.path
from django.utils import unittest
from contextlib import nested
from mock import patch, Mock
from nose.tools import eq_, ok_
from make_mozilla.base.tests.decorators import wip, integration
from make_mozilla.bsd.tests.utils import json_fixture

from django.conf import settings
from make_mozilla import bsd
from make_mozilla.events import models
import urllib2
import json

class MockHTTPResponse(object):
    def __init__(self, headers = {}):
        self._headers = dict([(k.lower(), v) for (k,v) in headers.items()])

    def getheader(self, name, default):
        return self._headers.get(name.lower(), default)

class BSDEventFeedParserTest(unittest.TestCase):
    @patch.object(bsd, 'parse_event_feed')
    @patch.object(bsd.BSDEventImporter, 'process_event')
    def test_that_the_event_feed_can_be_fetched_and_processed(self, 
            mock_process_func, mock_feed_parser):
        mock_feed_parser.return_value = ['rtw']

        bsd.fetch_and_process_event_feed('http://feed.url/')

        mock_feed_parser.assert_called_with('http://feed.url/')
        mock_process_func.assert_called_with('rtw')

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

        eq_(['w2d', 'w2p', 'w9l', 'w9w', 'w9q', 'wcz'], actual)

class BSDClientTest(unittest.TestCase):
    @patch.object(bsd, 'BSDApiFactory')
    def test_that_bsdapi_is_instantiated_correctly(self, mock_api_factory):
        orig_settings = settings.BSD_API_DETAILS
        settings.BSD_API_DETAILS = {'id': 'api_user', 'secret': 'sekrit', 
                'host': 'api.host.org'}
        try:
            mock_api_factory_instance = Mock()
            mock_api_factory.return_value = mock_api_factory_instance
            mock_api_client = Mock()
            mock_api_factory_instance.create.return_value = mock_api_client

            client = bsd.BSDClient.create_api_client()

            mock_api_factory_instance.create.assert_called_with(
                        id = 'api_user', secret = 'sekrit', host = 'api.host.org',
                        port = 80, securePort = 443)
            eq_(client, mock_api_client)
        finally:
            settings.BSD_API_DETAILS = orig_settings

    @patch.object(bsd.BSDClient, 'create_api_client')
    def test_that_a_get_request_can_be_performed(self,
            mock_client_func):
        mock_client = Mock()
        mock_client_func.return_value = mock_client
        mock_response = Mock()
        mock_client.doRequest.return_value = mock_response

        eq_(mock_response,
                bsd.BSDClient._get('/api_method', {'params': 'dict'}))

        mock_client.doRequest.assert_called_with('/api_method',
                api_params = {'params': 'dict'},
                https = True,
                request_type = 'GET')

    @patch.object(bsd.BSDClient, 'create_api_client')
    def test_that_a_post_request_can_be_performed(self,
            mock_client_func):
        mock_client = Mock()
        mock_client_func.return_value = mock_client
        mock_response = Mock()
        mock_client.doRequest.return_value = mock_response

        eq_(mock_response,
                bsd.BSDClient._post('/api_method', {'params': 'dict'}))

        mock_client.doRequest.assert_called_with('/api_method',
                api_params = {'params': 'dict'},
                https = True,
                request_type = 'POST')

    def test_that_encoding_can_be_extracted_from_api_response(self):
        mock_response = Mock()
        mock_response.http_response = MockHTTPResponse({'Content-Type': 'text/xml; charset=UTF-8'})
        eq_(bsd.BSDClient._api_response_charset(mock_response), 'UTF-8')

    def test_that_encoding_extracted_from_api_response_without_charset_defaults_to_utf_8(self):
        mock_response = Mock()
        mock_response.http_response = MockHTTPResponse({'Content-Type': 'text/xml'})
        eq_(bsd.BSDClient._api_response_charset(mock_response), 'utf-8')

    def test_that_encoding_extracted_from_api_response_without_content_type_defaults_to_utf_8(self):
        mock_response = Mock()
        mock_response.http_response = MockHTTPResponse()
        eq_(bsd.BSDClient._api_response_charset(mock_response), 'utf-8')

    @patch.object(bsd.extractors.xml, 'constituent_email')
    @patch.object(bsd.BSDClient, '_api_response_charset')
    @patch.object(bsd.BSDClient, '_get')
    def test_that_constituent_email_can_be_queried_given_a_cons_id(self,
            mock_client_func,
            mock_charset_func,
            mock_email_extractor_func):
        mock_response = Mock()
        mock_client_func.return_value = mock_response
        mock_charset_func.return_value = 'utf-8'
        mock_response.body  = '<xml>'
        mock_email_extractor_func.return_value = 'example@mozilla.org'

        eq_('example@mozilla.org', 
                bsd.BSDClient.constituent_email_for_constituent_id('abcd'))

        mock_client_func.assert_called_with('/cons/get_constituents_by_id',
                {'cons_ids': 'abcd', 'bundles': 'primary_cons_email'})
        mock_charset_func.assert_called_with(mock_response)
        mock_email_extractor_func.assert_called_with('<xml>')

    @patch.object(bsd.BSDClient, '_get')
    def test_that_event_can_be_fetched_given_obfuscated_id(self,
            mock_client_func):
        mock_api_response = Mock()
        mock_client_func.return_value = mock_api_response
        mock_api_response.body = '{"event": "json"}'

        eq_(bsd.BSDClient.fetch_event('obf_id'), {'event': 'json'})

        mock_client_func.assert_called_with('/event/get_event_details', 
                {'values': json.dumps({'event_id_obfuscated': 'obf_id'})})

    @patch.object(bsd.BSDClient, '_post')
    def test_that_organiser_email_can_be_added_as_constituent(self,
            mock_client_func):
        mock_api_response = Mock()
        mock_client_func.return_value = mock_api_response
        mock_api_response.http_status = 200
        mock_api_response.body = '{"cons_id"  : 34, "email_id" : 234}'

        eq_(34, bsd.BSDClient.register_email_address_as_constituent('example@mozilla.org'))

        mock_client_func.assert_called_with('/cons/email_register', 
                {'email': 'example@mozilla.org', 'format': 'json'})

    @patch.object(bsd.BSDClient, '_post')
    def test_that_constituent_id_can_be_added_to_constituent_group(self,
            mock_client_func):
        mock_api_response = Mock()
        mock_client_func.return_value = mock_api_response
        mock_api_response.http_status = 202

        ok_(bsd.BSDClient.add_constituent_id_to_group('1234', '111'))

        mock_client_func.assert_called_with('/cons_group/add_cons_ids_to_group', 
                {'cons_ids': '1234', 'cons_group_id': '111'})

class BSDRegisterConstituentTest(unittest.TestCase):
    @patch.object(bsd.BSDClient, 'add_constituent_id_to_group')
    @patch.object(bsd.BSDClient, 'register_email_address_as_constituent')
    def test_email_is_registered_and_added_to_group(self, mock_register_func, mock_group_func):
        mock_register_func.return_value = 34
        mock_group_func.return_value = True

        ok_(bsd.BSDRegisterConstituent.add_email_to_group('example@mozilla.org', '1234'))

        mock_register_func.assert_called_with('example@mozilla.org')
        mock_group_func.assert_called_with(34, '1234')

class BSDEventImporterTest(unittest.TestCase):
    def setUp(self):
        self.importer = bsd.BSDEventImporter()

    @patch.object(bsd.BSDClient, 'fetch_event')
    def test_that_an_event_can_be_processed(self, mock_client_func):
        klass = bsd.BSDEventImporter
        with patch.object(bsd, 'BSDEventImporter') as MockEventImporter:
            mock_event_importer = Mock()
            MockEventImporter.return_value = mock_event_importer
            mock_client_func.return_value = {'event': 'json'}

            klass.process_event('obf_id')

            mock_client_func.assert_called_with('obf_id')
            mock_event_importer.process_event_from_json.assert_called_with({'event': 'json'})

    @patch.object(bsd, 'Event')
    def test_that_the_importer_can_import_a_new_event(self, MockEvent):
        with nested(
                patch.object(self.importer, 'event_source_id'),
                patch.object(self.importer, 'fetch_existing_event'),
                patch.object(self.importer, 'fetch_organiser_email_from_bsd'),
                patch.object(self.importer, 'venue_for_event'),
                patch.object(self.importer, 'new_models_from_json'),
                patch.object(self.importer, 'are_model_instances_identical')
            ) as (mock_source_id_func, mock_fetch_event_func,
                    mock_fetch_organiser_func, mock_venue_func,
                    mock_new_models_func, mock_identical_func):
            event_json = {'event': 'json'}
            mock_null_event = Mock()
            mock_event = Mock()
            mock_null_venue = Mock()
            mock_venue = Mock()

            mock_fetch_event_func.return_value = None
            MockEvent.return_value = mock_null_event
            mock_source_id_func.return_value = 'source_id'
            mock_fetch_organiser_func.return_value = 'example@mozilla.org'
            mock_venue_func.return_value = mock_null_venue
            mock_new_models_func.return_value = (mock_event, mock_venue)
            mock_identical_func.return_value = False

            self.importer.process_event_from_json(event_json)

            MockEvent.assert_called_with()
            mock_source_id_func.assert_called_with(event_json)
            mock_fetch_event_func.assert_called_with('source_id')
            mock_fetch_organiser_func.assert_called_with(event_json)
            mock_venue_func.assert_called_with(mock_null_event)
            mock_new_models_func.assert_called_with(event_json)
            ok_(((mock_null_event, mock_event),) in mock_identical_func.call_args_list)
            ok_(((mock_null_venue, mock_venue),) in mock_identical_func.call_args_list)
            mock_event.save.assert_called
            mock_venue.save.assert_called

    def test_that_the_event_source_id_can_be_extracted(self):
        eq_(self.importer.event_source_id({'event_id': '1'}), 'bsd:1')

    @patch.object(bsd.Event, 'objects')
    def test_that_an_event_can_be_fetched_from_db_if_this_is_a_reimport(self, mock_event_objects):
        mock_event = Mock()
        mock_event_objects.get.return_value = mock_event

        eq_(self.importer.fetch_existing_event('source_id'), mock_event)

        mock_event_objects.get.assert_called_with(source_id = 'source_id')

    @patch.object(bsd.Event, 'objects')
    def test_that_no_event_is_fetched_if_this_is_a_new_import(self, mock_event_objects):
        mock_event_objects.get.side_effect = bsd.Event.DoesNotExist()

        ok_(self.importer.fetch_existing_event('source_id') is None)

        mock_event_objects.get.assert_called_with(source_id = 'source_id')
    
    @patch.object(bsd.BSDClient, 'constituent_email_for_constituent_id')
    def test_that_organiser_email_can_be_pulled_from_BSD_API(self, mock_api_func):
        mock_api_func.return_value = 'example@mozilla.org'

        eq_(self.importer.fetch_organiser_email_from_bsd({'creator_cons_id': 'abcd'}),
                'example@mozilla.org')

        mock_api_func.assert_called_with('abcd')

    def test_that_the_venue_for_an_existing_event_is_returned(self):
        mock_event = Mock()
        mock_venue = Mock()
        mock_event.venue = mock_venue

        eq_(self.importer.venue_for_event(mock_event), mock_venue)

    @patch.object(bsd, 'Venue')
    def test_that_the_venue_for_an_existing_event_is_returned(self, MockVenue):
        mock_venue = Mock()
        MockVenue.return_value = mock_venue

        eq_(self.importer.venue_for_event(None), mock_venue)
        MockVenue.assert_called_with()

    def test_that_identical_model_instances_can_be_compared_properly(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = 1, name = "Hallo")

        ok_(self.importer.are_model_instances_identical(e1, e2))

    def test_that_non_identical_model_instances_compare_false(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = 1, name = "Boo hoo")

        ok_(not self.importer.are_model_instances_identical(e1, e2))

    def test_that_model_instances_of_different_classes_compare_false(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Venue(id = 1, name = "Hallo")

        ok_(not self.importer.are_model_instances_identical(e1, e2))

    def test_that_unset_ids_are_ignored_when_comparing_instances(self):
        e1 = models.Event(id = 1, name = "Hallo")
        e2 = models.Event(id = None, name = "Hallo")

        ok_(self.importer.are_model_instances_identical(e1, e2))

    @patch.object(bsd, 'Venue')
    @patch.object(bsd, 'Event')
    def test_that_event_and_venue_objects_can_be_created_from_the_json(self,
            MockEvent, MockVenue):
        with patch.object(self.importer, 'extract_from_event_json') as mock_extract_func:
            mock_extract_func.return_value = {'event': {'attr': 1}, 'venue': {'attr': 2}}
            mock_event = Mock()
            mock_venue = Mock()
            MockEvent.return_value = mock_event
            MockVenue.return_value = mock_venue

            eq_(self.importer.new_models_from_json({'event': 'json'}), 
                    (mock_event, mock_venue))

            mock_extract_func.assert_called_with({'event': 'json'})
            MockEvent.assert_called_with(attr = 1)
            MockVenue.assert_called_with(attr = 2)

    def test_relevant_information_can_be_extracted_from_event_json(self):
        with nested(
                patch.object(self.importer, 'event_extractors'),
                patch.object(self.importer, 'venue_extractors')
            ) as (mock_event_extractors, mock_venue_extractors):
            event_json = json_fixture('event.json')
            mock_event_extractor = Mock()
            mock_venue_extractor = Mock()
            mock_event_extractors.return_value = [mock_event_extractor]
            mock_venue_extractors.return_value = [mock_venue_extractor]
            mock_event_extractor.return_value = {1: 1}
            mock_venue_extractor.return_value = {2: 2}
            expected = {'event': {1: 1}, 'venue': {2: 2}}

            actual = self.importer.extract_from_event_json(event_json)

            mock_event_extractor.assert_called_with(event_json)
            mock_venue_extractor.assert_called_with(event_json)
            eq_(expected, actual)

