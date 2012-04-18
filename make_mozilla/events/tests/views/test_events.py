from django.utils import unittest
from mock import patch, Mock
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.http import QueryDict

from django.conf import settings
from django.core.urlresolvers import resolve, reverse
import jingo

from make_mozilla.events.views import events
from make_mozilla.events import forms

c = Client()
rf = RequestFactory()

class TestEventViewsNew(unittest.TestCase):
    def test_that_it_routes(self):
        self.assertIs(resolve('/events/new').func, events.new)

    @patch('make_mozilla.events.forms.VenueForm')
    @patch('make_mozilla.events.forms.EventForm')
    @patch('jingo.render')
    def test_that_it_renders_with_the_correct_forms(self, mock_render, MockEventForm, MockVenueForm):
        event_form = Mock()
        venue_form = Mock()
        MockEventForm.return_value = event_form
        MockVenueForm.return_value = venue_form
        request = rf.get('/events/new')
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
        self.assertIs(resolve('/events/create').func, events.create)

    def test_that_it_rejects_get_requests(self):
        request = rf.get('/events/create')
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

        request = rf.post('/events/create', self.data)
        events.create(request)

        mock_func.assert_called_with(query_dict_from(self.data))

    @patch.object(events, 'process_create_post_data')
    @patch.object(events, 'create_event_and_venue')
    def test_that_valid_data_creates_an_event_and_venue_and_redirects(self, mock_create_func, mock_forms_func):
        mock_forms_func.return_value = (self.mock_ef, self.mock_vf)
        mock_create_func.return_value = (mock_persisted_event(id = 1), None)

        request = rf.post('/events/create', self.data)
        response = events.create(request)

        expected_redirect_url = reverse('event', kwargs={'event_id': 1})
        mock_create_func.assert_called_with(self.mock_ef, self.mock_vf)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], expected_redirect_url)

    def test_that_create_event_and_venue_does_that_given_valid_data(self):
        ef = forms.EventForm(self.data)
        vf = forms.VenueForm(self.data)

        event, venue = events.create_event_and_venue(ef, vf)

        self.assertIsNotNone(event.id)
        self.assertIsNotNone(venue.id)
        self.assertEqual(venue, event.venue)

