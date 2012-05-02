from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django import http
import urlparse, urllib
import jingo

from django_browserid.forms import BrowserIDForm

from make_mozilla.users.models import UserProfile

def _extract_redirect_destination(request):
    if not request.GET.has_key('next'): return {'post_verify_qs': ''}
    return {'post_verify_qs': '?next=' + urllib.quote_plus(urlparse.urlparse(request.GET['next']).path, safe = '/')}


def login(request):
    return jingo.render(request, 'login.html', _extract_redirect_destination(request))
