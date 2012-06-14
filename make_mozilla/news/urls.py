from django.conf.urls.defaults import patterns, url

from make_mozilla.news import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='news'),
)
