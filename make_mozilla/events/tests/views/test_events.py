from django.utils import unittest
from mock import patch, Mock
from django.test import TestCase
from nose.tools import eq_, ok_
from django.test.client import Client, RequestFactory
from django.http import QueryDict
from make_mozilla.base.tests.assertions import assert_routing, assert_redirects_to_named_url

from django.conf import settings
from django.core.urlresolvers import resolve, reverse
import jingo

from make_mozilla.events import views as events
from make_mozilla.events import forms
from make_mozilla.events import models

c = Client()
rf = RequestFactory()

class TestEventViewsIndex(unittest.TestCase):
    def test_that_it_routes(self):
        assert_routing('/events/', events.index, name = 'events')

class TestIndexGeoRSSFeed(unittest.TestCase):
    def setUp(self):
        self.feed = events.IndexGeoRSSFeed()

    def test_that_it_routes(self):
        assert_routing('/events/feed.rss', events.IndexGeoRSSFeed, name = 'events-feed')

    def test_that_it_correctly_fetches_the_item_geometry(self):
        mock_item = Mock()
        mock_item.location = 'location'

        eq_('location', self.feed.item_geometry(mock_item))

    def test_that_it_returns_the_correct_url(self):
        eq_(self.feed.link, reverse('events'))

    @patch.object(models.Event, 'upcoming')
    def test_that_it_correctly_returns_upcoming_events_for_items(self, mock_query_method):
        mock_item = Mock()
        mock_query_method.return_value = [mock_item]

        eq_(self.feed.items(), [mock_item])

class TestEventViewsNew(unittest.TestCase):
    def test_that_it_routes(self):
        assert_routing('/events/new/', events.new, name = 'event.new')

    @patch('make_mozilla.events.forms.VenueForm')
    @patch('make_mozilla.events.forms.EventForm')
    @patch('jingo.render')
    def test_that_it_renders_with_the_correct_forms(self, mock_render, MockEventForm, MockVenueForm):
        event_form = Mock()
        venue_form = Mock()
        MockEventForm.return_value = event_form
        MockVenueForm.return_value = venue_form
        request = rf.get('/events/new/')
        events.new(request)

        mock_render.assert_called_with(request, 'events/new.html', {'event_form': event_form, 'venue_form': venue_form})

def valid_form(valid = True):
    form = Mock()
    form.is_valid.return_value = valid
    return form

def invalid_form():
    return valid_form(False)

def query_dict_from(data_dict):
    qd = QueryDict('', mutable = True)
    qd.update(data_dict)
    return qd

def mock_persisted_event(id = 1):
    mock_event = Mock()
    mock_event.id = id
    return mock_event

class TestEventViewsCreate(TestCase):
    def setUp(self):
        self.data = {
            'event-name': 'Test Event',
            'event-url': 'http://example.com/',
            'venue-name': 'Test Venue',
            'venue-street_address': '100 Test Street',
            'venue-country': 'UK',
            'venue-latitude': '51.0',
            'venue-longitude': '0.5'
        }
        self.mock_ef = valid_form()
        self.mock_vf = valid_form()

    def test_that_it_routes(self):
        assert_routing('/events/create/', events.create, name = 'event.create')

    def test_that_it_rejects_get_requests(self):
        request = rf.get('/events/create/')
        response = events.create(request)
        self.assertEqual(405, response.status_code)

    @patch.object(forms, 'EventForm')
    @patch.object(forms, 'VenueForm')
    def test_that_form_helper_correctly_instantiates_form_objects_from_post_data(self, MockVenueForm, MockEntryForm):
        MockEntryForm.return_value = self.mock_ef
        MockVenueForm.return_value = self.mock_vf

        ef, vf = events.process_create_post_data(self.data)

        MockEntryForm.assert_called_with(self.data)
        MockVenueForm.assert_called_with(self.data)
        self.assertEqual(ef, self.mock_ef)
        self.assertEqual(vf, self.mock_vf)

    @patch.object(events, 'process_create_post_data')
    def test_that_it_correctly_processes_the_post_data(self, mock_func):
        mock_func.return_value = (invalid_form(), invalid_form())

        request = rf.post('/events/create/', self.data)
        events.create(request)

        mock_func.assert_called_with(query_dict_from(self.data))

    @patch.object(events, 'process_create_post_data')
    @patch.object(events, 'create_event_and_venue')
    def test_that_valid_data_creates_an_event_and_venue_and_redirects(self, mock_create_func, mock_forms_func):
        mock_forms_func.return_value = (self.mock_ef, self.mock_vf)
        mock_create_func.return_value = (mock_persisted_event(id = 1), None)

        request = rf.post('/events/create/', self.data)
        response = events.create(request)

        mock_create_func.assert_called_with(self.mock_ef, self.mock_vf)
        assert_redirects_to_named_url(response, 'event', kwargs = {'event_id': 1})

    def test_that_create_event_and_venue_does_that_given_valid_data(self):
        ef = forms.EventForm(self.data)
        vf = forms.VenueForm(self.data)

        event, venue = events.create_event_and_venue(ef, vf)

        self.assertIsNotNone(event.id)
        self.assertIsNotNone(venue.id)
        self.assertEqual(venue, event.venue)

    @patch.object(events, 'process_create_post_data')
    @patch.object(events, 'create_event_and_venue')
    @patch('jingo.render')
    def test_that_invalid_data_causes_a_rerender_of_the_new_template(self, mock_render, mock_create_func, mock_forms_func):
        ef = invalid_form()
        vf = invalid_form()
        mock_forms_func.return_value = (ef, vf)

        request = rf.post('/events/create/', self.data)
        response = events.create(request)

        mock_create_func.assert_not_called()
        mock_render.assert_called_with(request, 'events/new.html', {'event_form': ef, 'venue_form': vf})

class TestEventViewsDetail(unittest.TestCase):
    def test_that_it_routes_correctly(self):
        assert_routing('/events/abcde/', events.details, name = 'event', kwargs = {'event_id': 'abcde'})

    @patch.object(models.Event.objects, 'get')
    @patch('jingo.render')
    def test_that_it_correctly_fetches_the_event(self, mock_render, mock_event_get):
        mock_event = Mock()
        mock_event_get.return_value = mock_event
        request = rf.get('/events/abcde')
        events.details(request, event_id = 'abcde')

        mock_render.assert_called_with(request, 'events/detail.html', {'event': mock_event})
        mock_event_get.assert_called_with(pk = 'abcde')
