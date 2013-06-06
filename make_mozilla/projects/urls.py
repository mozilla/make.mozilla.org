from django.conf.urls.defaults import patterns, url
from make_mozilla.projects import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='projects'),
    url(r'(?P<slug>[\w-]+)/$',
        views.details,              name='project'),
)
