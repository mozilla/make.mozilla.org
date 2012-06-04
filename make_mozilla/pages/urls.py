from django.conf.urls.defaults import patterns, url
from make_mozilla.pages import views

urlpatterns = patterns('',
    url(r'^(.+)/$',
        views.serve,                name='page'),
)