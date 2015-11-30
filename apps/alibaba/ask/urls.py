from django.conf.urls import patterns, url, include

urlpatterns = patterns('ask.views',
    url(r'^$', "index", name='ask_home'),
    url(r'^(?P<pk>[0-9A-Za-z]+).html$', "detail", name='ask_detail'),
)