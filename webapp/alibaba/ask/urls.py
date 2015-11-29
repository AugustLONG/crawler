from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "ask.views.index", name='ask_home'),
    url(r'^(?P<pk>[0-9A-Za-z]+).html$', "ask.views.detail", name='ask_detail'),
]