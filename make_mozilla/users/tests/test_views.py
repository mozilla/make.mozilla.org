from django.conf import settings
from django.utils import unittest

from mock import patch, Mock
from nose.tools import eq_, ok_
from make_mozilla.base.tests.assertions import assert_routing

from make_mozilla.users import views

class LoginJumpPageTest(unittest.TestCase):
    def test_that_it_routes(self):
        assert_routing('/users/login/', views.login, name = 'login')

