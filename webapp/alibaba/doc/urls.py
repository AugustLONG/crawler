from django.conf.urls import patterns, url, include

urlpatterns = patterns('doc.views',
    url(r'^$', "index", name='doc_home'),
    url(r'^$', "detail", name='doc_detail'),
    )