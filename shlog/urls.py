from django.conf.urls import *

urlpatterns = patterns('shlog.views',
    url(r'^$', 'full_blog', name='app_main'),
)