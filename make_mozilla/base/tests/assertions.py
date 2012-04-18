from nose.tools import eq_, ok_
from django.core.urlresolvers import resolve, reverse

def assert_routing(url, view_function, name = '', kwargs = {}):
    resolved_route = resolve(url)
    ok_(resolved_route.func is view_function)
    if kwargs:
        eq_(resolved_route.kwargs, kwargs)
    if name:
        eq_(reverse(name, kwargs = kwargs), url)

def assert_redirects_to_named_url(response, name, kwargs = {}, permanent = False):
    status_codes = {True: 301, False: 302}
    expected_redirect_url = reverse(name, kwargs = kwargs)
    eq_(response.status_code, status_codes[permanent])
    eq_(response['Location'], expected_redirect_url)
