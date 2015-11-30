from django.conf.urls import patterns, url, include

urlpatterns = patterns('library.views',
    url(r'^$', "index", name='library_home'),
    url(r'^$', "detail", name='library_detail'),
    )