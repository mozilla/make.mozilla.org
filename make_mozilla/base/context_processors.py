from urllib import urlencode
from urlparse import urljoin

from django.conf import settings

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import QueryDict


def login_and_get_back(request):
    """Build a target URL for the login page to send the user back to after login.
    
    Where possible, we want to keep the user on the page they're currently on.
    """
    def login_url_with_return_path():
        login_url = reverse('login')
        qd = QueryDict('', mutable=True)
        qd[REDIRECT_FIELD_NAME] = request.get_full_path()
        query_string = qd.urlencode(safe='/')
        return urljoin(login_url, '?' + query_string)
    return {'login_url': login_url_with_return_path}
