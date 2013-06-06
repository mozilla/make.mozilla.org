from django.conf.urls.defaults import patterns, url
from make_mozilla.users import views

urlpatterns = patterns('',
    url(r'^login/$', views.login, name = 'login'),
)
