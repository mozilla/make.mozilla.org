from django.utils import unittest
from mock import patch, Mock
from contextlib import nested
from django.test import TestCase
from nose.tools import eq_, ok_
from django.test.client import Client, RequestFactory
from django.http import QueryDict
from make_mozilla.base.tests.assertions import assert_routing, assert_redirects_to_named_url

from django.conf import settings
from django.core.urlresolvers import resolve, reverse
import jingo

from make_mozilla.events import views
from make_mozilla.events import forms
from make_mozilla.events import models
from make_mozilla.events import paginators

c = Client()
rf = RequestFactory()

class TestEventViewsIndex(unittest.TestCase):
    def test_that_it_routes(self):
        assert_routing('/events/', views.index, name = 'events')

class TestIndexGeoRSSFeed(unittest.TestCase):
    def setUp(self):
        self.feed = views.IndexGeoRSSFeed()

    def test_that_it_routes(self):
        assert_routing('/events/feed.rss', views.IndexGeoRSSFeed, name = 'events-feed')

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
        assert_routing('/events/new/', views.new, name = 'event.new')

    @patch.object(forms, 'PrivacyAndLegalForm')
    @patch.object(forms, 'VenueForm')
    @patch.object(forms, 'EventForm')
    @patch.object(views, '_render_event_creation_form')
    def test_that_it_renders_with_the_correct_forms(self, mock_render, MockEventForm, MockVenueForm, MockPrivacyAndLegalForm):
        event_form = Mock()
        venue_form = Mock()
        privacy_and_legal_form = Mock()
        privacy_and_legal_form = Mock()
        MockEventForm.return_value = event_form
        MockVenueForm.return_value = venue_form
        MockPrivacyAndLegalForm.return_value = privacy_and_legal_form
        request = rf.get('/events/new/')
        request.user = Mock()
        views.new(request)

        mock_render.assert_called_with(request, event_form, venue_form, privacy_and_legal_form)

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
            'venue-country': 'GB',
            'venue-latitude': '51.0',
            'venue-longitude': '0.5'
        }
        self.mock_ef = valid_form()
        self.mock_vf = valid_form()
        self.mock_lf = valid_form()

    def test_that_it_routes(self):
        assert_routing('/events/create/', views.create, name = 'event.create')

    def test_that_it_rejects_get_requests(self):
        request = rf.get('/events/create/')
        response = views.create(request)
        self.assertEqual(405, response.status_code)

    @patch.object(forms, 'PrivacyAndLegalForm')
    @patch.object(forms, 'EventForm')
    @patch.object(forms, 'VenueForm')
    def test_that_form_helper_correctly_instantiates_form_objects_from_post_data(self, 
            MockVenueForm, MockEntryForm, MockPrivacyAndLegalForm):
        MockEntryForm.return_value = self.mock_ef
        MockVenueForm.return_value = self.mock_vf
        MockPrivacyAndLegalForm.return_value = self.mock_lf

        ef, vf, lf = views._process_create_post_data(self.data)

        MockEntryForm.assert_called_with(self.data)
        MockVenueForm.assert_called_with(self.data)
        MockPrivacyAndLegalForm.assert_called_with(self.data)
        self.assertEqual(ef, self.mock_ef)
        self.assertEqual(vf, self.mock_vf)
        self.assertEqual(lf, self.mock_lf)

    @patch.object(views, '_process_create_post_data')
    @patch('jingo.render')
    def test_that_it_correctly_invokes_the_form_processor(self, mock_render, mock_forms_func):
        mock_forms_func.return_value = (invalid_form(), invalid_form(), invalid_form())

        request = rf.post('/events/create/', self.data)
        request.user = Mock()
        views.create(request)

        mock_forms_func.assert_called_with(query_dict_from(self.data))

    @patch.object(views.tasks, 'register_email_address_as_constituent')
    def test_that_helper_adds_email_to_BSD_if_permission_was_given(self, mock_task_func):
        mock_user = Mock()
        mock_user.email = 'example@mozilla.org'
        mock_privacy_form = Mock()
        mock_privacy_form.cleaned_data = {'add_me_to_email_list': True}

        views._add_email_to_bsd(mock_user, mock_privacy_form)

        mock_task_func.delay.assert_called_with('example@mozilla.org', '111')

    @patch.object(views.tasks, 'register_email_address_as_constituent')
    def test_that_helper_does_not_add_email_to_BSD_if_permission_refused(self, mock_task_func):
        mock_user = Mock()
        mock_user.email = 'example@mozilla.org'
        mock_privacy_form = Mock()
        mock_privacy_form.cleaned_data = {'add_me_to_email_list': False}

        views._add_email_to_bsd(mock_user, mock_privacy_form)

        eq_(mock_task_func.delay.call_args_list, [])

    @patch.object(views, '_add_email_to_bsd')
    @patch.object(views, '_process_create_post_data')
    @patch.object(views, '_create_event_and_venue')
    def test_that_valid_data_creates_an_event_and_venue_and_redirects(self, mock_create_func, 
            mock_forms_func, mock_bsd_email_func):
        mock_forms_func.return_value = (self.mock_ef, self.mock_vf, self.mock_lf)
        mock_create_func.return_value = (mock_persisted_event(id = 1), None)
        mock_user = Mock()

        request = rf.post('/events/create/', self.data)
        request.user = mock_user
        response = views.create(request)

        mock_bsd_email_func.assert_called_with(mock_user, self.mock_lf)
        mock_create_func.assert_called_with(mock_user, self.mock_ef, self.mock_vf)
        assert_redirects_to_named_url(response, 'event', kwargs = {'event_id': 1})

    def test_that_create_event_and_venue_does_that_given_valid_data(self):
        event_kind = models.EventKind(name = "Test", slug = "test", description = "Test")
        event_kind.save()
        self.data['event-kind'] = str(event_kind.id)
        ef = forms.EventForm(self.data)
        vf = forms.VenueForm(self.data)
        mock_user = Mock()
        mock_user.email = 'example@mozilla.org'

        event, venue = views._create_event_and_venue(mock_user, ef, vf)

        ok_(event.id is not None)
        ok_(venue.id is not None)
        eq_(venue.location.y, 51.0)
        eq_(venue, event.venue)

    @patch.object(views, '_add_email_to_bsd')
    @patch.object(views, '_process_create_post_data')
    @patch.object(views, '_create_event_and_venue')
    @patch.object(views, '_render_event_creation_form')
    def test_that_invalid_data_causes_a_rerender_of_the_new_template(self, mock_render, mock_create_func,
            mock_forms_func, mock_bsd_email_func):
        ef = invalid_form()
        vf = invalid_form()
        lf = invalid_form()
        mock_forms_func.return_value = (ef, vf, lf)

        request = rf.post('/events/create/', self.data)
        request.user = Mock()
        response = views.create(request)

        eq_(mock_create_func.call_args_list, [])
        eq_(mock_bsd_email_func.call_args_list, [])
        mock_render.assert_called_with(request, ef, vf, lf)

class TestEventViewsDetail(unittest.TestCase):
    def test_that_it_routes_correctly(self):
        assert_routing('/events/12/', views.details, name = 'event', kwargs = {'event_id': '12'})

    @patch.object(views, 'get_object_or_404')
    @patch('jingo.render')
    def test_that_it_correctly_fetches_the_event(self, mock_render, mock_event_get):
        mock_event = Mock()
        mock_event_get.return_value = mock_event
        request = rf.get('/events/1')
        views.details(request, event_id = '1')

        mock_render.assert_called_with(request, 'events/detail.html', {'event': mock_event})
        mock_event_get.assert_called_with(models.Event, pk = '1')

class TestEventViewsNear(unittest.TestCase):
    def test_that_it_routes_correctly_for_the_map(self):
        assert_routing('/events/near/map/', views.near_map, name = 'events.near.map')

    def test_that_it_routes_correctly_for_the_list(self):
        assert_routing('/events/near/', views.near, name = 'events.near')

    def setUp(self):
        self.near = views.Near()
        self.mock_page = Mock()

    def test_that_latlon_search_params_are_extracted(self):
        (lat, lon) = self.near.extract_latlon(rf.get('/?lat=51.0&lng=-0.4'))
        eq_(lat, '51.0')
        eq_(lon, '-0.4')

    def test_that_page_defaults_to_1(self):
        eq_(1, self.near.extract_page(rf.get('/')))

    def test_that_sort_defaults_to_date(self):
        (sort, order) = self.near.extract_sort(rf.get('/'))
        eq_(sort, 'date')
        eq_(order, 'start')

    def test_that_sort_search_param_is_extracted(self):
        (sort, order) = self.near.extract_sort(rf.get('/?sort=name'))
        eq_(sort, 'name')
        eq_(order, 'name')

    def test_that_page_is_returned_verbatim_if_present(self):
        eq_('fnord', self.near.extract_page(rf.get('/?page=fnord')))

    @patch.object(models.Event, 'near')
    @patch.object(paginators, 'results_page')
    def test_that_results_page_is_correctly_returned(self,
            mock_results_page, mock_query):
        mock_query_set = Mock()
        mock_query.return_value = mock_query_set
        mock_paginated_results = Mock()
        mock_results_page.return_value = mock_paginated_results

        eq_(self.near.paginated_results('lat', 'lon', 'order', 999, 1),
                mock_paginated_results)

        mock_query.assert_called_with('lat', 'lon', sort = 'order')
        mock_results_page.assert_called_with(mock_query_set, 999, page = 1)

    @patch('jingo.render')
    def test_that_a_template_can_be_rendered_correctly(self,
            mock_render):
        with nested(
                patch.object(self.near, 'extract_latlon'),
                patch.object(self.near, 'extract_page'),
                patch.object(self.near, 'extract_sort'),
                patch.object(self.near, 'paginated_results')
                ) as (mock_latlon, mock_page, mock_sort, mock_results):
            request = rf.get('/')
            mock_paginated_results = Mock()
            mock_latlon.return_value = ('lat', 'lon')
            mock_page.return_value = 1
            mock_sort.return_value = ('sort', 'order')
            mock_results.return_value = mock_paginated_results
            mock_response = Mock()
            mock_render.return_value = mock_response

            self.near.render(request, 'template-path', 999)

            mock_latlon.assert_called_with(request)
            mock_page.assert_called_with(request)
            mock_results.assert_called_with('lat', 'lon', 'order', 999, 1)
            mock_render.assert_called_with(request, 'template-path', {
                'results': mock_paginated_results,
                'latitude': 'lat',
                'longitude': 'lon',
                'sort': 'sort',
            })

    @patch.object(views.near_view, 'render')
    def test_that_it_correctly_renders_for_maps(self, 
            mock_near_view):
        mock_response = Mock()
        mock_near_view.return_value = mock_response
        request = rf.get('/events/near?lat=51.0&lng=-0.4')

        eq_(views.near_map(request), mock_response)
        mock_near_view.assert_called_with(request, 'events/near-map.html', 24)

    @patch.object(views.near_view, 'render')
    def test_that_it_correctly_renders_for_lists(self, 
            mock_near_view):
        mock_response = Mock()
        mock_near_view.return_value = mock_response
        request = rf.get('/events/near?lat=51.0&lng=-0.4')

        eq_(views.near(request), mock_response)
        mock_near_view.assert_called_with(request, 'events/near-list.html', 4)
