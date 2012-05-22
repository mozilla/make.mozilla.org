from django.conf.urls.defaults import patterns, url
from make_mozilla.tools import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='tools'),
    url(r'(?P<slug>[\w-]+(?:-[\w-]+)*)/$',
        views.details,              name='tool'),
)