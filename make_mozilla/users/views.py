from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django import http

from django_browserid.auth import get_audience
from django_browserid.forms import BrowserIDForm

from make_mozilla.users.models import UserProfile

def _verify_assertion(form):
    if not form.is_valid():
        return None
    return form.cleaned_data['assertion']

def _authenticate_from_assertion(assertion, request):
    user = auth.authenticate(assertion=assertion,
                             audience=get_audience(request))

# @require_POST
def verify(request):
    form = BrowserIDForm(request.POST)
    assertion = _verify_assertion(form)
    if assertion is not None:
        user = _authenticate_from_assertion(assertion, request)
        if user is not None and user.is_active:
            auth.login(request, user)
            return http.HttpResponseRedirect(reverse('events'))
    # should be a redirect to some kind of failed login page here...
