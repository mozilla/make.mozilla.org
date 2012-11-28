from django.conf.urls.defaults import patterns, url

from make_mozilla.static_pages import views

urlpatterns = patterns('',
    url(r'^itu/$', views.itu_index, name='itu_index'),
    url(r'^itu/kit/$', views.itu_kit, name='itu_kit'),
    url(r'^itu/advocates/$', views.itu_advocates, name='itu_advocates'),
    url(r'^itu/videos/$', views.itu_videos, name='itu_videos'),
)
