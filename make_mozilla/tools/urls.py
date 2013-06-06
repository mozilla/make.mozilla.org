from django.conf.urls.defaults import patterns, url
from make_mozilla.tools import views

urlpatterns = patterns('',
    url(r'^$',
        views.index,                name='tools'),
    url(r'x-ray-goggles/$',
        views.details_goggles,      name='tool.goggles'),
    url(r'x-ray-goggles/install/$',
        views.details_goggles_install, name='tool.goggles.install'),
    # url(r'(?P<slug>[\w-]+(?:-[\w-]+)*)/$',
    #     views.details,              name='tool'),
)
