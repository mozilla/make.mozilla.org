from django.test import TestCase
from mock import patch, Mock
from django.test.client import RequestFactory
import lxml.html
from lxml.cssselect import CSSSelector

# from django.conf import settings
# from django.core.urlresolvers import resolve
import jingo

from make_mozilla.events.views import events
from make_mozilla.events import forms

# c = Client()
rf = RequestFactory()

class WithinElementContext:
    def __init__(self, context_node):
        self.context_node = context_node

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _select(self, selector_string):
        if self.context_node is None:
            return None
        selector = CSSSelector(selector_string)
        node_list = selector(self.context_node)
        if len(node_list) > 0:
            return node_list[0]
        else:
            return None

    def has_css(self, selector_string):
        return self._select(selector_string) is not None

    def within_css(self, selector_string):
        return WithinElementContext(self._select(selector_string))

def html_context(html_string):
    root_context = lxml.html.fromstring(html_string)
    return WithinElementContext(root_context)

class TestEventsNewTemplate(TestCase):
    def setUp(self):
        self.ef = forms.EventForm()
        self.vf = forms.VenueForm()
        self.request = rf.get('/events/new')
        context = {'event_form': self.ef, 'venue_form': self.vf}
        self.result = jingo.render(self.request, 'events/new.html', context)
        self.html = html_context(self.result.content)

    def test_the_page_contains_form_pointed_at_events_create(self):
        assert self.html.has_css('form[action=/events/create]')

    def test_the_page_contains_the_event_form_fields(self):
        with self.html.within_css('form[action=/events/create]') as html:
            assert html.has_css('input[name]')

