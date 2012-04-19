from django.conf.urls.defaults import patterns, url
from make_mozilla.users import views

urlpatterns = patterns('',
    url(r'^verify$', views.verify, name = 'browserid-verify'),
)

