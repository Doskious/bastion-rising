from django.conf.urls import *

urlpatterns = patterns('ehtest.views',
    url(r'^$', 'explorer_view', name='app_main'),
)