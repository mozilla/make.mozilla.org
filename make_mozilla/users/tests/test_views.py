from django.conf import settings
from django.utils import unittest

from mock import patch, Mock
from nose.tools import eq_, ok_
from django.test.client import RequestFactory
import django_browserid.forms
from make_mozilla.base.tests.assertions import assert_routing, assert_redirects_to_named_url

from make_mozilla.users.models import UserProfile
from make_mozilla.users import views

rf = RequestFactory()

class BrowserIDVerificationTest(unittest.TestCase):
    def setUp(self):
        self.active_mock_user = Mock()
        self.active_mock_user.is_active = True

    def test_that_it_routes(self):
        assert_routing('/users/verify', views.verify, name = 'browserid-verify')

    @patch.object(views, '_authenticate_from_assertion')
    @patch.object(views, '_verify_assertion')
    @patch.object(views, 'BrowserIDForm')
    def test_that_login_is_not_attempted_with_an_invalid_browser_id_assertion(self,
            mock_form_class, mock_verify_func, mock_authenticate_func):

        mock_form = Mock()
        mock_form_class.return_value = mock_form
        mock_verify_func.return_value = None
        request = rf.post('/verify')

        views.verify(request)

        mock_form_class.assert_called_once_with(request.POST)
        mock_verify_func.assert_called_once_with(mock_form)
        mock_authenticate_func.assert_not_called()

    @patch.object(views.auth, 'login')
    @patch.object(views, '_authenticate_from_assertion')
    @patch.object(views, '_verify_assertion')
    def test_that_authentication_is_attempted_with_a_valid_browser_id_assertion(self,
            mock_verify_func, mock_authenticate_func, mock_django_auth_login):

        mock_verify_func.return_value = 'valid_assertion'
        mock_authenticate_func.return_value = None
        request = rf.post('/verify')

        views.verify(request)

        mock_authenticate_func.assert_called_once_with('valid_assertion', request)
        mock_django_auth_login.assert_not_called()

    @patch.object(views.auth, 'login')
    @patch.object(views, '_authenticate_from_assertion')
    @patch.object(views, '_verify_assertion')
    def test_that_user_is_logged_in_with_valid_assertion_and_located_user(self,
            mock_verify_func, mock_authenticate_func, mock_django_auth_login):
        mock_verify_func.return_value = 'valid_assertion'
        mock_authenticate_func.return_value = self.active_mock_user
        request = rf.post('/verify')

        views.verify(request)

        mock_django_auth_login.assert_called_once_with(request, self.active_mock_user)

    @patch.object(views.auth, 'login')
    @patch.object(views, '_authenticate_from_assertion')
    @patch.object(views, '_verify_assertion')
    def test_that_successful_login_redirects_to_events_index(self,
            mock_verify_func, mock_authenticate_func, mock_django_auth_login):
        mock_verify_func.return_value = 'valid_assertion'
        mock_authenticate_func.return_value = self.active_mock_user
        request = rf.post('/verify')

        response = views.verify(request)

        assert_redirects_to_named_url(response, 'events')
