from django.conf.urls import patterns, url, include

urlpatterns = patterns('soft.views',
    url(r'^$', "index", name='soft_home'),
    url(r'^$', "detail", name='soft_detail'),
    )