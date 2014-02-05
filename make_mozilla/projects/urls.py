from django.conf.urls.defaults import patterns, url
from make_mozilla.projects import views

urlpatterns = patterns('',
    url(r'^groups/(?P<slug>[\w-]+)/$',
        views.group,                name='group'),
    url(r'^$',
        views.index,                name='projects'),
    url(r'(?P<slug>[\w-]+)/$',
        views.details,              name='project'),
)
