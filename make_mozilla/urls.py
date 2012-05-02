from django.conf import settings
from django.conf.urls.defaults import *

from funfactory.monkeypatches import patch
patch()

import make_mozilla.events.urls
import make_mozilla.users.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$',          'make_mozilla.base.views.root.index'),
    url(r'^events/',    include(make_mozilla.events.urls)),
    url(r'^users/',     include(make_mozilla.users.urls)),
    # browserid endpoints
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', kwargs={'next_page': '/events/'}, name='logout'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
