from django.test import TestCase
from mock import patch, Mock
from django.test.client import RequestFactory
from bs4 import BeautifulSoup

# from django.conf import settings
# from django.core.urlresolvers import resolve
import jingo

from make_mozilla.events.views import events
from make_mozilla.events import forms

# c = Client()
rf = RequestFactory()

class TestEventsNewTemplate(TestCase):
    def setUp(self):
        self.ef = forms.EventForm()
        self.vf = forms.VenueForm()
        self.request = rf.get('/events/new')
        context = {'event_form': self.ef, 'venue_form': self.vf}
        self.result = jingo.render(self.request, 'events/new.html', context)
        self.soup = BeautifulSoup(self.result.content, 'lxml')

    def test_the_page_contains_form_pointed_at_events_create(self):
        assert len(self.soup.select('form[action=/events/create]')) > 0

    def test_the_page_contains_the_event_form_fields(self):
        assert len(self.soup.select('form[action=/events/create]')[0].select('input[name]')) > 0

