from django.conf.urls.defaults import patterns, url
from make_mozilla.projects import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='projects'),
    url(r'^submit/$',
        views.submit,               name='project.submit'),
    url(r'(?P<project_hash>[a-z0-9]{9,})/$',
        views.details,              name='project'),
)