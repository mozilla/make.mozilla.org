from django.conf import settings
from django.utils import unittest

from django.test.client import Client, RequestFactory
from mock import patch, Mock
from nose.tools import eq_, ok_
from make_mozilla.base.tests.assertions import assert_routing

from make_mozilla.users import views

rf = RequestFactory()

class LoginJumpPageTest(unittest.TestCase):
    def test_that_it_routes(self):
        assert_routing('/users/login/', views.login, name = 'login')

    @patch('jingo.render')
    def test_that_redirect_url_is_correctly_inserted_into_the_context(self, mock_render):
        request = rf.get('/users/login/', {'next': '/a/url'})

        views.login(request)

        mock_render.assert_called_with(request, 'login.html', {'post_verify_qs': '?next=/a/url'})
