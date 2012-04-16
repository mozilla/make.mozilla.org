from django.utils import unittest
from mock import patch, Mock
from django.test.client import Client, RequestFactory

from django.conf import settings
from django.core.urlresolvers import resolve
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

