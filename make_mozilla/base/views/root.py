from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import jingo


def index(request):
    return HttpResponseRedirect(reverse('events'))


def fail(request):
    return jingo.render(request, 'base/404.html', {}, status=404)


def app_fail(request):
    return jingo.render(request, 'base/500.html', {}, status=500)

