from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponseRedirect(reverse('events'))

